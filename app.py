"""Example flask app that stores passwords in clear text. Yikes."""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask-notes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    '''redirect to register'''
    return redirect('/register')


@app.route('/register', methods=['GET', "POST"])
def register():
    '''show the homepage that allows a user to register'''

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return redirect('/secret')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''show the login for our app'''

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
    
        user = User.authenticate(username, password)

        if user:
            session['user_id'] = user.id
            return redirect('/secret')
    
        else:
            form.username.errors = ['Bad name/password']
    
    return render_template('login.html', form=form)



@app.route('/secret')
def show_secret_page():
    '''display secret page to logged in users'''

    return render_template('secrets.html')