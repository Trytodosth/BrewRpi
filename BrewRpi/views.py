"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from BrewRpi import app
from BrewRpi.Beer import *
import BrewRpi.Server


myBeer = Beer()


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    global myBeer
    return render_template('brewery.html',
        myBeer=myBeer, IP = BrewRpi.Server.get_ip(), updatetime=BrewRpi.Server.get_time())

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template('contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.')

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.')



@app.route("/mashing")
def page_mashing():
    """Renders the Mashing page."""
    global myBeer

    return render_template('mashing.html',
        myBeer=myBeer, IP = BrewRpi.Server.get_ip(), updatetime=BrewRpi.Server.get_time())




@app.route("/start/step=<step>&ind=<ind>")
def start_brewing():
    """Attempt at starting a new brewing step."""
    global myBeer
    
    was_started, mess = myBeer.start_step(ind)
    if was_started:
        return redirect(url_for('/'))

    return render_template('mashing.html',
        myBeer=myBeer, IP = BrewRpi.Server.get_ip(), updatetime=BrewRpi.Server.get_time())

    return redirect(url_for('/'))