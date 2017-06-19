# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
   
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True,nullable=False)
    username = db.Column(db.String(60), index=True, unique=True,nullable=False)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(128),nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    outfits = db.relationship('Outfit', backref='user', lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Outfit(db.Model):
   
    __tablename__ = 'outfits'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sex = db.Column(db.String(1),nullable=False)
    photo = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(180))
    is_public = db.Column(db.Boolean, default=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Outfit: {}>'.format(self.name)

class Genre(db.Model):
    
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    description = db.Column(db.String(200))
    outfits = db.relationship('Outfit', backref='genre', lazy='dynamic')
    

    def __repr__(self):
        return '<Genre: {}>'.format(self.name)
