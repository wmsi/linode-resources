#!/usr/bin/python
from flask import Flask, request, render_template, send_file, redirect, url_for, flash, jsonify, Response
from app import app, forms, db, base#, socketio
from app.models import User, Post, DataStory, ProjectMetaData
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
from include.credentials import AIRTABLE_API_KEY

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
            user.data_story = True
            # only for testing, this should be more secure
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

    if request.args.get('project_id'):
        project_id = request.args.get('project_id', type=int)
        project = []
        ds = DataStory.query.filter(DataStory.archived!=True, DataStory.project_id==project_id).all()
        for d in ds:
            data = {}
            data['project_id']=project_id
            data['data_type']=d.data_type
            data['timestamp']=str(d.timestamp)
            data['value']=d.value
            project.append(data)

        return json.dumps(project)
    # datastory = DataStory.query.filter(DataStory.archived!=True).all()
    return render_template('data_story.html', title='Digital Data Stories', project_names=get_project_names(), bgcolor='black')

# Serve static project pages for the public to access, 
# without as many headers or options for editing data
@app.route('/project/<int:project_id>')
def static_project(project_id):
    project_data = DataStory.query.filter_by(project_id=project_id).all()
    app.logger.warning('rendering project with ' + str(len(project_data)) + ' data points')
    if len(project_data) == 0:
        return render_template('page_not_found.html')
    return render_template('static_project.html', title='Project Page', datastory=project_data, bgcolor='black', project_id=project_id)

@app.route('/load-csv',methods=['POST','GET'])
@login_required
def load_csv():
    pmd = ProjectMetaData.query.all()
    new_id = pmd[len(pmd)-1].id+1
    if request.method == 'POST':
        if request.is_json:
            content = request.get_json()
            project_id = int(content[0]['project_id']) if 'project_id' in content[0] else new_id
            for item in content:
                data_type = str(item['data_type'])
                sensor_id = int(item['sensor_id'])
                timestamp = dateutil.parser.parse(item['timestamp'])
                value = float(item['value'])
                data = DataStory(timestamp=timestamp, project_id=project_id, data_type=data_type, sensor_id=sensor_id, value=value)
                db.session.add(data)
                # print(data)
            db.session.commit()

            pmd = ProjectMetaData.query.filter_by(id=project_id).all()
            if(len(pmd) == 0):
                pmd = ProjectMetaData(id=project_id, project_name=('Project ' + str(project_id)))
                db.session.add(pmd)
                db.session.commit()
            # print(request.get_json())
            project_str = 'new project' if project_id == new_id else 'project'
            return 'loaded ' + str(len(content)) + ' values to a ' + project_str + ' with id ' + str(project_id)
        else:
            return 'something went wrong :('
    if request.args.get('next_id'):
        return str(new_id)
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

# Crop some values from an existing project in the database into a new project
@app.route('/crop-project', methods=['POST'])
def crop_project():
    pmd = ProjectMetaData.query.all()
    new_id = pmd[len(pmd)-1].id+1
    project_name = request.form.get('name')
    if(project_name is None or project_name == ""):
        project_name = 'Project ' + str(new_id)
    # app.logger.warning('new project name ' + project_name)
    pmd = ProjectMetaData(project_name=project_name, description=request.form.get('desc'), miscellaneous=request.form.get('misc'))
    db.session.add(pmd)
    db.session.commit()

    data = json.loads(request.form.get('data'))
    for datum in data:
        ds = DataStory(project_id=new_id)
        ds.data_type = datum["data_type"]
        ds.value = datum["value"]
        ds.timestamp =  dateutil.parser.parse(datum['timestamp'])
        db.session.add(ds)
        db.session.commit()

    return 'created cropped project with id ' + str(new_id) + ' and name ' + project_name

# Handle all HTTP requests from Scratch.
# These blocks exist as part of the WMSI DBBlocks extensions for scratch3
# available on our scratch-vm fork at:
# https://github.com/wmsi/scratch-vm/tree/develop/src/extensions/scratch3_db_blocks
# These blocks allow users to push new data to the database and
# retrieve a list of all data that meet certain attributes (specified
# in Scratch)
@app.route('/scratch', methods=['POST','GET'])
def scratch():
    if request.method == 'POST':
    # add some validation/ security screening here
        # project_id = request.form.get('project_id')
        # sensor_id = request.form.get('sensor_id')
        # data_type = request.form.get('data_type')
        # value = request.form.get('value')
        if(request.form.get('pmd')):
            return edit_meta_data(request)

        return post_data_value(request)

    if request.method == 'GET':
        # project_id = request.args.get('project_id')
        # data_type = request.args.get('data_type')
        # add support for project meta data

        if(request.args.get('pmd')):
            # sample_pmd = '{"name": "test", "id": 0, "description": "example project", "miscellaneous": "", "data_sets": {"tempF": [69.0], "tempC": [22.0, 30.0]}}'
            # return sample_pmd
            return get_meta_data(request.args.get('project_id'), request.args.get('data'))
        if(request.args.get('project_names')):
            return get_project_names()
        return get_project_data(request)


@app.route('/scratch-gui')
def scratch_gui():
    return render_template('scratch_gui.html')
    # return render_template('scratch-build/index.html')

@app.route('/resource-table')
def resource_tabl():
    return send_from_directory(app.config["RESOURCE_TABLE"], "resource_table.json")

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



####################################### STEM Resource ROUTES #######################################
# These routes were added starting 1/19/20 to handle secure Airtable API requests for the STEM resource site
# These may eventually be transferred to a serverless HTTP Proxy like Cloud Cloud Functions
@app.route("/airtable", methods=['POST','GET'])
def airtable():
    if request.method == 'GET':
        results = []
        fields_to_del = ['Grade Range','Rating','Search Text','Rating','Votes','id','New Comments'];
        page_size = 100 # default
        query = request.args.get('query')
        if request.args.get('offset'):
            return multi_page_load(request)
        else:            
            for record in base.get_all(formula=query):
                # only return desired fields
                for field in fields_to_del:
                    if field in record['fields']:
                        del record['fields'][field]
                results.append(record['fields'])
            print('returning ' + str(len(results)) + ' results')
            return json.dumps(results)
        # return json.dumps(base.get_all(formula=query, page_size=page_size))

    if request.method == 'POST':
        print('request with args ', json.dumps(request.form))
        # add exception handling here
        record_id = request.form.get('id')
        record = base.get(record_id)
        fields = {}

        # Ratings are deprecated
        if request.form.get('Rating'):
            fields = {'Rating': float(request.form.get('Rating')), 'Votes': int(request.form.get('Votes'))}
        elif request.form.get('Comment'):
            fields = post_comment(record, 'Comment')

        # this is the new default so we can review comments before they go live
        elif request.form.get('New Comment'):
           fields = post_comment(record, 'New Comment')

        print('updating ', str(record_id), ' with ', json.dumps(fields))
        return json.dumps(base.update(record_id, fields))

# Load first page, then remaining results for a given query
# This helps front end speed, by allowing the site to load page 1
# of results then store the rest
# @param {object} request - HTTP Request
# @returns {object} repsonse object to be returned from view
def multi_page_load(request):
    page_size = request.args.get('page_size')
    query = request.args.get('query')
    num_results = 0
    results = []
    fields_to_del = ['Grade Range','Rating','Search Text','Rating','Votes','id','New Comments'];

    base_iter = base.get_iter(formula=query, page_size=page_size)
    for i, page in enumerate(base_iter):
        num_results += len(page)
        if ((i == 0) if request.args.get('offset') == 'false' else (i != 0)):
            # print('adding records from page ' + str(i))
            for record in page:
                 # only return desired fields
                for field in fields_to_del:
                    if field in record['fields']:
                        del record['fields'][field]
                results.append(record['fields'])

    resp = jsonify(results)
    resp.headers['page_size'] = page_size 
    resp.headers['num_results']= num_results 
    resp.headers['Access-Control-Expose-Headers'] = 'page_size,num_results'
    # print('returning remaining with n=' + str(num_results))
    return resp

# Post a comment to Airtable for the given record
# 'field_key' can either be 'Comments' or 'New Comments'
# @param {object} record - Airtable record to udpate
# @param {string} key - (value of either 'Comment' or 'New Comment') used for 
#       retrieving comment from request and posting to Airtable 
def post_comment(record, key):
    field_key = key + 's'
    print("posting " + request.form.get(key) + " to " + field_key)
    if field_key in record['fields']:
        comments = record['fields'][field_key] + ', '
    else:
        comments = ''
    comments = comments + request.form.get(key)
    return {field_key: comments}


# DEPRECATED due to separate multi_page_load function and difficulties sorting
# Return one page of results with the specificed page size and page number
# This function is deprecated due to difficulties getting results one page at a time
# when they've already been sorted on the site. We may bring this back as a way to 
# speed up response time, by rendering the first page while other results are being returned
def get_page_resp(request):
    page_size = request.args.get('page_size')
    page_num = 0 if request.args.get('page_num') is None else int(request.args.get('page_num'))
    query = request.args.get('query')
    num_results = 0
    results = []
    fields_to_del = ['Grade Range','Rating','Search Text','Rating','Votes','id','New Comments'];

    print('querying base with page size ' + str(page_size) + ', page num ' + str(page_num))
    base_iter = base.get_iter(formula=query, page_size=page_size)
    for i, page in enumerate(base_iter):
        num_results += len(page)
        if i == page_num:
            for record in page:
                 # only return desired fields
                for field in fields_to_del:
                    if field in record['fields']:
                        del record['fields'][field]
                results.append(record['fields'])
    resp = jsonify(results)
    resp.headers['num_results']= num_results 
    resp.headers['Access-Control-Expose-Headers'] = 'num_results'
    print('returning first page response')
    return resp








### SPECIAL ###

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

def get_meta_data(project_id, data=True):
    pmd = ProjectMetaData.query.filter_by(id=project_id).all()
    data_set = DataStory.query.filter(DataStory.project_id==int(project_id), DataStory.archived==False).all()
    if(pmd == []):
        pmd = ProjectMetaData(id=project_id, project_name=str(project_id))
    else:
        pmd = pmd[0]
    project = {}
    project['name'] = pmd.project_name
    project['id'] = pmd.id
    project['description'] = pmd.description
    project['miscellaneous'] = pmd.miscellaneous
    if data != 'false':
        project['data_sets'] = {}
        for datum in data_set:
            if datum.data_type not in project['data_sets']:
                project['data_sets'][datum.data_type] = []
            project['data_sets'][datum.data_type].append(datum.value)
    app.logger.warning('returning project ' + project_id + ' with data=' + str(data) + ' and len ' + str(len(data_set)))
    json_data = json.dumps(project)
    return json_data

def edit_meta_data(request):
    project_id = int(request.form.get('project_id'))
    msg = ''
    pmd = ProjectMetaData.query.filter_by(id=project_id)
    if(pmd == []):
        return 'no project with id ' + str(project_id)
    pmd = pmd[0]
    if(request.form.get('name')):
        msg = msg + 'replaced name of project ' + str(project_id) + ' with "' + request.form.get('name') + '"; '
        pmd.project_name = request.form.get('name')
    if(request.form.get('description')):
        msg = msg + 'replaced description of project ' + str(project_id) + ' with "' + request.form.get('description') + '"; '
        pmd.description = request.form.get('description')
    if(request.form.get('miscellaneous')):
        msg = msg + 'replaced miscellaneous field of project ' + str(project_id) + ' with "' + request.form.get('miscellaneous') + '";'
        pmd.miscellaneous = request.form.get('miscellaneous')

    db.session.add(pmd)
    db.session.commit()
    return msg

def post_data_value(request):
    # app.logger.warning('proj id: ' + request.form.get('project_id'))
    project_id = int(request.form.get('project_id'))
    sensor_id = request.form.get('sensor_id')
    data_type = request.form.get('data_type')
    value = request.form.get('value')

    data = DataStory(project_id=project_id, data_type=str(data_type), sensor_id=int(sensor_id), value=float(value))
    pmd = ProjectMetaData.query.filter_by(id=project_id).all()
    if(pmd == []):
        project_name = 'Project ' + str(project_id)
        pmd = ProjectMetaData(id=project_id, project_name=project_name)
        db.session.add(pmd)
    db.session.add(data)
    db.session.commit()
    # app.logger.warning("project_id: %s, data_type: %s, value: %s" \
        # % (str(project_id), str(data_type), str(value)))

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

def get_project_names():
    pmd = ProjectMetaData.query.all()
    project_names = []
    for project in pmd:
        if(len(DataStory.query.filter_by(project_id=project.id).all()) > 0):
            info = {}
            info['id'] = project.id
            info['name'] = project.project_name
            project_names.append(info)
    # project_names = json.dumps(project_names)
    # app.logger.warning('returning project names: ' + str(project_names))
    return project_names

# def send_new_value(data):
#     new_val = {}
#     new_val['project_id'] = str(data.project_id)
#     new_val['sensor_id'] = str(data.sensor_id)
#     new_val['data_type'] = str(data.data_type)
#     new_val['timestamp'] = format_datetime(data.timestamp)
#     new_val['value'] = str(data.value)
#     json_value = json.dumps(new_val)
    
#     socketio.emit('new value', json_value)
