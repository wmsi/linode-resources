#!/usr/bin/python
from flask import Flask, request, render_template, send_file, redirect, url_for, flash, jsonify
from app import app, forms, db
from app.models import User, Post, DataStory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import subprocess
import iot.press_button as pressButton
import logging
from logging.handlers import RotatingFileHandler
from include.utils import *
from include.config import *
from include.school_subdomains import *

DEFAULT_SUBDOMAIN = "www"

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

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
 
### SCHOOL SUBDOMAIN ROUTES ###

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

### DATA STORIES ###

# this is where routes associated with the Digital Data Stories project
# live. POSTs can be received from a ScratchX project hooked up to a sensor
# **ideally** using the standard form validation. GET requests will return 
# a web page rendering all the data collected so far. At some point we
# should separate data into different web pages or add an option for 
# selecting a dataset.

@app.route('/data-story', methods=['GET', 'POST'])
@login_required
def data_story():
    # hopefully this works with ScratchX, meaning that we're secured by our secret key
    form = forms.DataForm()
    if form.validate_on_submit():
        # add new data point to the DATASTORY table
        return "Yay new data!\n" # user never sees this 
    if current_user.data_story != True:
        flash("""Sorry, only users with project permissions can see this page. 
                If you believe your account should be activated with permissions 
                contact a WMSI administrator to make the change""")
        return redirect(url_for('forum'))
    datastory = DataStory.query.all()
    return render_template('data_story.html', title='Digital Data Stories', datastory=datastory, bgcolor='black')


@app.route('/scratchx', methods=['POST','GET'])
def scratchx():
    if request.method == 'POST':
    # add some validation/ security screening here
        project_id = request.form.get('project_id')
        sensor_id = request.form.get('sensor_id')
        data_type = request.form.get('data_type')
        value = request.form.get('value')

        data = DataStory(project_id=int(project_id), data_type=str(data_type), sensor_id=int(sensor_id), value=float(value))
        db.session.add(data)
        db.session.commit()
        app.logger.warning("project_id: %s, data_type: %s, value: %s" \
            % (str(project_id), str(data_type), str(value)))
        return "Thanks for posting! Your data has been added to https://wmsinh.org/data-story\n"
    if request.method == 'GET':
        project_id = request.args.get('project_id')
        data_type = request.args.get('data_type')
        if data_type is None:
            data_set = DataStory.query.filter_by(project_id=int(project_id)).all()
        else:
            data_set = DataStory.query.filter_by(project_id=int(project_id), data_type=str(data_type)).all()
        values = [];
        for datum in data_set:
            values.append(datum.value)
        return jsonify(values)


## IOT ROUTES ###

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
