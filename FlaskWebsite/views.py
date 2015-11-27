"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, url_for, request
from FlaskWebsite import app

from FlaskWebsite.models.redisClient import Client

client = Client()

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

# neue URL: www.seite.de/create - GET
@app.route("/create", methods = ["GET", "POST"])
def create():
    if request.method == 'GET':
        # send user the form
        return render_template(
            "CreateQuestion.html", 
            title='Create Question',
            year = datetime.now().year,
            message = 'Create your question here' 
            )
    elif request.method == 'POST':
        # read form-data and save it
        title = request.form["title"]
        question = request.form["question"] 
        answer = request.form["answer"]

        # Speichern in der Datenbank in der Form (question, answer) 
        client.saveQuestion(title, question, answer)

        # Aufruf des Templates mit Parameter aus dem Template
        return render_template("CreatedQuestion.html", question = question)
    else:
        return "<h2>Invalid request.</h2>"

# server/question/<title> nutzt title als Uebergabewert - POST
@app.route("/rquestion/", methods = ["GET", "POST"])
def rquestion():
    if request.method == "GET":

        # Get new Question
        client.resetTitle()
        title = client.getTitle()

        # Get random question title
        question = client.getQuestion(title)

        return render_template("AnswerQuestion.html", question = question, title = title) 
    elif request.method == "POST":

        # Get current question title
        title = client.getTitle()

        # User has attempted answer, check if correct
        submittedAnswer = request.form["submittedAnswer"]

        # Read answer form database
        answer = client.getAnswer(title)

        # reset title to random value
        client.resetTitle()

        if submittedAnswer == answer:
            return render_template("Correct.html")
        else:
            return render_template("Incorrect.html", submittedAnswer = submittedAnswer, answer = answer)
    else:
        return "<h2>Invalid request</h2>"

# server/question/<title> nutzt title als Uebergabewert - POST
@app.route("/question/<title>", methods = ["GET", "POST"])
def question(title):
    if request.method == "GET":
        # Get question from database
        question = client.getQuestion(title)
        
        # send user form
        return render_template("AnswerQuestion.html", question = question)

    elif request.method == "POST":
        # User has attempted answer, check if correct
        submittedAnswer = request.form["submittedAnswer"]

        # Read answer form database
        answer = client.getAnswer(title)
        if submittedAnswer == answer:
            return render_template("Correct.html")
        else:
            return render_template("Incorrect.html", submittedAnswer = submittedAnswer, answer = answer)
    else:
        return "<h2>Invalid request</h2>"


#@app.route("/adminhelp")
#def adminhelp():
#    m = "Message"
#    t = "Title"
#    return render_template("about.html", message = m, title = t)
