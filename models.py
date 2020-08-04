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
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        '''registers user with a hashed password and username'''

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return cls(username=username,
                    password=hashed,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        '''checks to see if a user is in our db'''

        user = User.query.filter(User.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False