# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class Usuario(UserMixin, db.Model):
   
    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True,nullable=False)
    username = db.Column(db.String(60), index=True, unique=True,nullable=False)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128),nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    vestuarios = db.relationship('Vestuario', backref='usuario', lazy='dynamic')

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
        return '<Usuario: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Vestuario(db.Model):
   
    __tablename__ = 'vestuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sexo = db.Column(db.String(1),nullable=False)
    foto = db.Column(db.String(150))
    genero_id = db.Column(db.Integer, db.ForeignKey('generos.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))

    def __repr__(self):
        return '<Vestuario: {}>'.format(self.name)

class Genero(db.Model):
    
    __tablename__ = 'generos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40), unique=True)
    description = db.Column(db.String(200))
    vestuarios = db.relationship('Vestuario', backref='genero', lazy='dynamic')
    

    def __repr__(self):
        return '<Genero: {}>'.format(self.name)