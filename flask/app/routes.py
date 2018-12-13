#!/usr/bin/python
from flask import Flask, request, render_template, send_file, redirect, url_for, flash, jsonify, Response
from app import app, forms, db#, socketio
from app.models import User, Post, DataStory#, ProjectMetaData
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
# from flask_socketio import emit, send
import subprocess
import iot.press_button as pressButton
import logging
import json
import time
import sys
import dateutil.parser
from logging.handlers import RotatingFileHandler
from include.utils import *
from include.config import *
from include.school_subdomains import *

DEFAULT_SUBDOMAIN = "www"

####################################### BASIC ROUTES #######################################
@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')
    
@app.route("/mobile")
def mobile():
    print("routing mobile")
    return render_template('mobile.html', 
        title="Mobile Programs")

@app.route("/all-locations")
def locations():
    return render_template('all-locations.html',    
        title="All WMSI Locations")

@app.route("/framegal")
@login_required
def framegal():
    frames = [
        {'src':'http://www.whitemountainscience.org'},
        {'src':'https://makezine.com/'},
        {'src':'https://www.sparkfun.com/'}
    ]
    for frame in frames:
        frame.name='name'
        frame.width='1200'
        frame.height='500'

    return render_template('iframe-gal.html', frames=frames)


#######################################  USER ROUTES #######################################
# These routes correspond to pages for registering new users, logging in, and logging out.
# User accounts are supported by the flask_login library
#
# To Do:
#   Add a route for deleting an account
#   Create a more secure method for adding user permissions
#   Add email confirmation for new users

# Handle user login. If login is sucessful, forward them to the page they
# were trying to access. Otherwise keep them on the login page.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# Use the built in flask_login fuction to logout the current user
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Add a new user account to the database
# If the user signs up with a @whitemountainscience.org email address
# set user.wmsi_user to True so they have full permissions on the site
# For now all new users are given access to the data_story page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        if "whitemountainscience.org" in user.email:
            user.wmsi_user = True
            # only for testing, this should be more secure
        user.data_story = True
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
 

####################################### SCHOOL SUBDOMAIN ROUTES #######################################

# for now always redirect to the gallery index for school subdomains
# (note: this must route /gallery/ with a _specific trailing
# slash_ to the index, because the various files in 
# gallery will redirect to gallery/ with the slash, and
# flask will return a 404 if we don't add that slash here
# (see here: http://flask.pocoo.org/docs/0.12/quickstart/#variable-rules))
@app.route("/", subdomain="<site_subdomain>")
def school_index(site_subdomain):
    return redirect("/gallery/") # direct redirect below

# make sure the root page displays the index
@app.route("/gallery/", subdomain="<site_subdomain>")
def subdomain_index(site_subdomain):
    return school_subdomain(site_subdomain, "index.html")

# any requests to gallery items for each subdomain are passed
# onto the correct school domain subfolder
# (thumbs up stores files and SETS LINKS assuming that 
#  files are stored under /gallery/, so we serve files 
#  statically (from the filesystem) from there)
@app.route("/gallery/<path:filename>", subdomain="<site_subdomain>")
def school_subdomain(site_subdomain, filename):
    if site_subdomain == DEFAULT_SUBDOMAIN: # www
        return redirect(url_for('index'))
    else:
        return serve_school_subdomain(site_subdomain, filename)



####################################### DATA STORIES #######################################
# This section contains routes associated with the Digital Data Stories project./
# POSTs can be received from a ScratchX project or by using a cURL command:
# curl -d "project_id=0&data_type=tempC&value=25" -X POST https://wmsinh.org/scratchx
# The /data-story route and data_story.html page are respondisble for rendering data


# Render the data_story.html page. In order to view the page, a user
# must have the data_story attribute set to true for their account. 
# While still in development this attribute is set to True for all
# new users
@app.route('/data-story',methods=['POST','GET'])
@login_required
def data_story():
    if current_user.data_story != True:
        flash("""Sorry, only users with project permissions can see this page. 
                If you believe your account should be activated with permissions 
                contact a WMSI administrator to make the change""")
        return redirect(url_for('index'))

    if request.method == 'POST':
        project_id = request.form.get('project_id')
        project = DataStory.query.filter_by(project_id=project_id).all()
        for datum in project:
            datum.archived = True
            db.session.add(datum)
        db.session.commit()
        return str('project ' + project_id + ' has been archived. To revive this project contact a system administrator')

    datastory = DataStory.query.filter(DataStory.archived!=True).all()
    return render_template('data_story.html', title='Digital Data Stories', datastory=datastory, bgcolor='black')

@app.route('/load-csv',methods=['POST','GET'])
@login_required
def load_csv():
    if request.method == 'POST':
        if request.is_json:
            content = request.get_json()
            for item in content:
                project_id = int(item['project_id'])
                data_type = str(item['data_type'])
                sensor_id = int(item['sensor_id'])
                timestamp = dateutil.parser.parse(item['timestamp'])
                value = float(item['value'])
                data = DataStory(timestamp=timestamp, project_id=project_id, data_type=data_type, sensor_id=sensor_id, value=value)
                db.session.add(data)
                print(data)
            
            db.session.commit()
            # print(request.get_json())
            return 'got some data!'
        else:
            return 'something went wrong :('
    if request.method == 'GET':
        return render_template('load_csv.html', title='Load CSV File', bgcolor='black')



# This route is pinged on a timer by the data_story page to get database updates
# The code below depends on both the web page and the server being on the same
# timer. In the past this has run into issues when the webpage and server clocks
# are set to different timezones
@app.route('/get_new_data')
def get_new_data():
    since = request.args.get('since', 0.0, type=float)
    all_data = DataStory.query.filter(DataStory.archived!=True).all()
    new_data = []
    time_float = None
    # app.logger.warning('checking for new data')
    for d in all_data:
        if (sys.version_info > (3, 0)):
            time_int = int(d.timestamp.timestamp()*1000)
        else:
            epoch = datetime.datetime.utcfromtimestamp(0)
            time_int = int((d.timestamp - epoch).total_seconds()*1000)
        if(time_int > since):
            app.logger.warning('found new data at ' + str(time_int))
            new_data.append({
                'project_id': d.project_id,
                'sensor_id': d.sensor_id,
                'timestamp': time_int,   # use this method to send the timestamp as an int
                'value': d.value,
                'data_type': d.data_type
            })
            # app.logger.warning('new data found at ' + str(d.timestamp.timestamp()))


    return jsonify(new_data)

# Handle all HTTP requests from Scratch.
# As of now the only working blocks exist as a ScratchX extension]
# These blocks allow users to push new data to the database and
# retrieve a list of all data that meet certain attributes (specified
# in Scratch)
@app.route('/scratchx', methods=['POST','GET'])
def scratchx():
    if request.method == 'POST':
    # add some validation/ security screening here
        project_id = request.form.get('project_id')
        sensor_id = request.form.get('sensor_id')
        data_type = request.form.get('data_type')
        value = request.form.get('value')
        if(request.form.get('pmd')):
            return edit_meta_data(request)

        return post_data_value(request)

    if request.method == 'GET':
        # project_id = request.args.get('project_id')
        # data_type = request.args.get('data_type')

        # add support for project meta data
        if(request.args.get('pmd')):
            sample_pmd = '{"name": "test", "id": 0, "description": "example project", "miscellaneous": "", "data_sets": {"tempF": [69.0], "tempC": [22.0, 30.0]}}'
            return sample_pmd
            # return get_meta_data(request.args.get('project_id'))
        return get_project_data(request)

@app.route('/scratch-gui')
def scratch_gui():
    return render_template('scratch-build/index.html')

@app.route('/static/assets/<path:path>')
def send_assets(path):
    return send_from_directory(app.config["SCRATCH_ASSETS"], path)

@app.route('/static/blocks-media/<path:path>')
def send_blocks(path):
    return send_from_directory(app.config["SCRATCH_BLOCKS"], path)

# socketio uses websocket which doesn't work with apache 
# but would be a great option if we ever change servers.
# With this we could remove timed polling and push new data from the server:
    # @socketio.on('connect')
    # def test_connect():
    #     emit('test response', {'data': 'test'})


####################################### FORUM ROUTES #######################################
# These routes were developed for a forum section prototype. Basic functionality is 
# outlined below, but more work would definitely be needed in order to add this feature
# to  the site 

@app.route("/forum", methods=['GET','POST'])
@login_required
def forum():
    form = forms.ForumForm()
    posts = Post.query.all()
    user = current_user
    if form.validate_on_submit():
        p = Post(body=form.body.data, author=user)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('forum'))
    style = """textarea {
            height: 10em;
            width: 35em;
            color: #000;
        }"""
    return render_template('forum.html', title='Community Forum', form=form, style=style, posts=posts)

@app.route('/edit-forum')
@login_required
def edit_forum():
    if current_user.wmsi_user != True:
        flash('Sorry, only registered WMSI users can edit the forum.')
        return redirect(url_for('forum'))
    form = forms.EditForm()
    posts = Post.query.all()
    return render_template('edit-forum.html', title='Edit Forum Posts', form=form, posts=posts)

@app.route('/delete-post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post is None:
        flash('Invalid Post ID. Could not delete.')
        return redirect(url_for('edit_forum'))
    db.session.delete(post)
    db.session.commit()
    flash('Success! Post "%s" deleted.' % post.body)
    return redirect(url_for('edit_forum'))

####################################### IOT ROUTES #######################################
# Built in December 2017, these routes support an Internet of Things example by communicating
# with a Labview VI connected to an EV3 robot

@app.route("/window")
def window():
    return render_template("iot-window.html", \
        title='Internet of Things', bgimg='static/img/Network.png')

@app.route("/press_button")
def pressbutton():
    pressButton.timeStamp()
    pressButton.sendRequest()
    return render_template('iot-waiting.html', \
        title='Internet of Things', bgimg='static/img/Network.png')

@app.route("/success")
def success():
    return render_template("iot-success.html", \
        title='Internet of Things', bgimg='static/img/Network.png')

@app.route("/labview", methods=['POST'])
def labview():
    subprocess.call('echo "%s" >> %s' \
        % (str(request.values['time']), IOT_STATUS_FILE), shell=True)
    print("from labview post: " + str(request.values['time']))
    return "Hello Labview\n"
    
@app.route("/iot/status")
def status():
    return send_file(IOT_STATUS_FILE, cache_timeout=0.5) # disable caching (mostly)

### SPECIAL ###

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# def get_meta_data(project_id):
#     pmd = ProjectMetaData.query.filter_by(id=project_id).all()
#     data_set = DataStory.query.filter(DataStory.project_id==int(project_id), DataStory.archived==False).all()
#     if(pmd == []):
#         pmd = ProjectMetaData(id=project_id, project_name=str(project_id))
#     else:
#         pmd = pmd[0]
#     project = {}
#     project['name'] = pmd.project_name
#     project['id'] = pmd.id
#     project['description'] = pmd.description
#     project['miscellaneous'] = pmd.miscellaneous
#     project['data_sets'] = {}
#     for datum in data_set:
#         if datum.data_type not in project['data_sets']:
#             project['data_sets'][datum.data_type] = []
#         project['data_sets'][datum.data_type].append(datum.value)
#     json_data = json.dumps(project)
#     return json_data

def edit_meta_data(request):
    project_id = int(request.form.get('project_id'))
    msg = ''
    # pmd = ProjectMetaData.query.filter_by(id=project_id)
    # if(pmd == []):
    #     return 'no project with id ' + str(project_id)
    # pmd = pmd[0]
    pmd = {}
    if(requst.form.get('name')):
        msg = 'replaced name of project ' + str(project_id) + ' with ' + requst.form.get('name')
        pmd.name = requst.form.get('name')
    elif(requst.form.get('description')):
        msg = 'replaced description of project ' + str(project_id) + ' with ' + requst.form.get('description')
        pmd.description = requst.form.get('description')
    elif(requst.form.get('miscellaneous')):
        msg = 'replaced miscellaneous field of project ' + str(project_id) + ' with ' + requst.form.get('miscellaneous')
        pmd.miscellaneous = requst.form.get('miscellaneous')

    # db.session.add(pmd)
    # db.session.commit()
    return msg

def post_data_value(request):
    data = DataStory(project_id=int(project_id), data_type=str(data_type), sensor_id=int(sensor_id), value=float(value))
    db.session.add(data)
    db.session.commit()
    app.logger.warning("project_id: %s, data_type: %s, value: %s" \
        % (str(project_id), str(data_type), str(value)))

    # send_new_value(data);
    # return "Thanks for posting! Your data has been added to https://wmsinh.org/data-story\n"
    # return str(data.timestamp.timestamp());
    return str(data.timestamp.strftime("%Y-%m-%d %H:%M:%S"));

def get_project_data(request):
    project_id = request.args.get('project_id')
    data_type = request.args.get('data_type')
    values = []

    if data_type is None:
        data_set = DataStory.query.filter(DataStory.project_id==int(project_id), DataStory.archived==False).all()
        for datum in data_set:
            values.append([datum.data_type, datum.value])
    else:
        data_set = DataStory.query.filter(DataStory.archived==False, DataStory.project_id==int(project_id), DataStory.data_type==str(data_type)).all()
        for datum in data_set:
            values.append(datum.value)
    return jsonify(values)

# def send_new_value(data):
#     new_val = {}
#     new_val['project_id'] = str(data.project_id)
#     new_val['sensor_id'] = str(data.sensor_id)
#     new_val['data_type'] = str(data.data_type)
#     new_val['timestamp'] = format_datetime(data.timestamp)
#     new_val['value'] = str(data.value)
#     json_value = json.dumps(new_val)
    
#     socketio.emit('new value', json_value)
