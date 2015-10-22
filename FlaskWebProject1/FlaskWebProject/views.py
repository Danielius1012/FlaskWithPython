"""
Routes and views for the flask application.
"""
from datetime import datetime
from flask import render_template, url_for, request
from FlaskWebProject import app


@app.route('/')
@app.route('/home')
def hello():
    """Renders a sample page."""
    return render_template(
        'home.html',
        title = 'Main Page',
        year = datetime.now().year,
        )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html'
    )


