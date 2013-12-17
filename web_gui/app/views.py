from flask import render_template, flash, redirect
from app import app
from forms import LoginForm, ConfigForm
import yaml
import os

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        { 
            'author': { 'nickname': 'John' }, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': { 'nickname': 'Susan' }, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
        title = 'Home',
	user = user,
        posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/config', methods = ['GET', 'POST'])
def config():
    form = ConfigForm()
    if form.validate_on_submit():
#        flash("" + str(form.temp_set.data) + " " +  str(form.temp_delta.data) + " " + str(form.valve_work.data) + " " + str(form.valve_delta.data))
        app.cfg['temp_set'] = float(form.temp_set.data)
        app.cfg['temp_delta'] = float(form.temp_delta.data)
        app.cfg['valve_work'] = float(form.valve_work.data)
        app.cfg['valve_delta'] = float(form.valve_delta.data)

        f=open('/home/pi/reletherm.cfg', 'w')
        yaml.dump(app.cfg,f)
        f.close()
        os.system('/home/pi/reletherm.py restart')
	
        return render_template('config.html', form = form, cfg = app.cfg, success = True)
    return render_template('config.html', form = form, cfg = app.cfg)
