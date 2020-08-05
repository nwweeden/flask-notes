"""Example flask app that stores passwords in clear text. Yikes."""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import User, db, connect_db, Note
from forms import RegisterForm, LoginForm, AddNoteForm, EditNoteForm

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

        users = User.query.all()
        # Query filter for user with the username

        for user in users:
            if user.username == username:
                flash("Username is already taken!")
                return render_template('register.html', form=form)
            if user.email == email:
                flash("Email is already taken!")
                return render_template('register.html', form=form)

                # form.username.errors.append("Username is already taken!")
        

        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return redirect(f'/users/{user.username}')

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
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Bad name/password']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log out the user and redirect to homepage."""

    session.pop("user_id")
    return redirect("/")


@app.route('/users/<username>')
def show_user_page(username):
    """Displays the current user's page and information."""

    if User.is_logged_in(username, session['user_id']):
        user = User.query.get(session['user_id'])
        return render_template("user.html", user=user)
    else:
        flash("You must be logged in as this user to view this page.")
        return redirect("/")


@app.route('/notes/<int:note_id>')
def show_note(note_id):
    """Displays the given note."""

    note = Note.query.get(note_id)
# FIXME Are we allowed to show anyone a note?
    return render_template("note.html", note=note)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes the user's account entirely."""

    notes = Note.query.filter(Note.owner == username).all()
    for note in notes:
        db.session.delete(note)
    db.session.commit()

    user = User.query.filter(User.username == username).first()
    db.session.delete(user)
    db.session.commit()
    flash("User deleted!")

    session.pop("user_id")

    return redirect("/")


@app.route('/users/<username>/notes/add', methods=['GET', 'POST'])
def show_add_note_form(username):
    """Display the add note form."""
#FIXME add authentication for user
    form = AddNoteForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)
        db.session.add(note)
        db.session.commit()
        flash("Note added!")

        return redirect(f"/users/{username}")

    else:
        return render_template("add_note_form.html", form=form, username=username)


@app.route('/notes/<int:note_id>/update', methods=['GET', 'POST'])
def show_edit_note_form(note_id):
    """Display the edit note form."""
    # If a route does more, add more to docstring in terms of description

    note = Note.query.get_or_404(note_id)
    form = EditNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash("Note edited!")
        return redirect(f"/users/{note.user.username}")

    else:
        return render_template("edit_note_form.html",
                               form=form,
                               note_id=note_id)


@app.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    """Delete the target note."""

    note = Note.query.get_or_404(note_id)

    username = note.user.username

    db.session.delete(note)
    db.session.commit()
    flash("Note deleted!")

    return redirect(f"/users/{username}")
