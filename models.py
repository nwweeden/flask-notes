from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    '''site user'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    #Good idea to put these on separate lines ^ If the code is more likely to change
    @classmethod
    def register(
            cls, 
            username, 
            password, 
            email, 
            first_name, 
            last_name,
            ):
        '''registers user with a hashed password and username'''

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(
            username=username,
            password=hashed,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    @classmethod
    def authenticate(cls, username, password):
        '''checks to see if a user is in our db'''

        user = User.query.filter(User.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    @classmethod
    def is_logged_in(cls, username, session_id):
        """Check to see if the user is logged in."""

        user = User.query.filter(User.username == username).first()

        return session_id == user.id

        # return true or false based on more specific conditions (ie user not in database combine with False)


class Note(db.Model):
    """Note."""

    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(20), db.ForeignKey(
        'users.username'), nullable=False)

    user = db.relationship("User", backref="notes")
