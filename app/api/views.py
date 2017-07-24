# app/admin/views.py
import json

from flask import abort, flash, redirect, render_template, url_for, jsonify, json, request
from flask_restful import Resource, request
from wtforms import Form, validators, StringField, PasswordField


from . import api
from .. import db
from ..models import Genre, User, Outfit

@api.route('/genres', methods=['GET', 'POST'])
def list_genres():
    genres = Genre.query.all()
    tasks = []
    for x in genres:
        tasks.append({
                'id': x.id,
                'name': x.name,
                'description': x.description        
              
        })
    return jsonify(tasks)

@api.route('/genres/show/<int:id>', methods=['GET', 'POST'])
def get_genre(id):
    add_genre = False
    returned_data = ""
    tasks = {}
    try:
        genre = Genre.query.get_or_404(id)  
        returned_data=[{
                'id': genre.id,
                'name': genre.name,
                'description': genre.description        
              
        }]
        
    except:
        returned_data=[{'error':'error'}]
    return jsonify(returned_data)   
            
    
    
@api.route('/genres/add', methods=['GET', 'POST'])
def add_genre():
    add_genre = True    
    returned_data = ""
    received_data = request.json
    try:
        gen = Genre(name=received_data['name'],description=received_data['description'])
        db.session.add(gen)
        db.session.commit()
        returned_data="Se creo nuevo genero"
    except:
        returned_data="Error ingresar genero"
    return returned_data

        
@api.route('/genres/edit/<int:id>', methods=['GET', 'POST', 'PUT'])
def edit_genre(id):
    add_genre = False
    returned_data = ""
    received_data = request.json
    try:
        genre = Genre.query.get_or_404(id)    
        genre.name = received_data['name']
        genre.description = received_data['description']
        db.session.commit()            
        returned_data="Se edito un genero"
    except:
        returned_data="Hubo un error al editar genero"
    return returned_data

@api.route('/genres/delete/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete_genre(id):
    returned_data = ""
    try:
        genre = Genre.query.get_or_404(id)
        db.session.delete(genre)
        db.session.commit()
        returned_data="Se elimino correctamente genero"
    except:
        returned_data="Hubo un error al eliminar genero"
    return returned_data
        

@api.route('/outfits', methods=['GET', 'POST'])
def list_outfits():
    outfits = Outfit.query.all()
    tasks = []
    for x in outfits:
        tasks.append({
                'id': x.id,
                'sex': x.sex,
                'photo': x.photo,
                'description': x.description,
                'is_public': x.is_public,
                'genre_id': x.genre_id,
                'user_id': x.user_id              
        })
    return jsonify(tasks)

@api.route('/outfits/show/<int:id>', methods=['GET', 'POST'])
def get_outfit(id):
    add_outfit = False
    returned_data = ""
    tasks = {}
    try:
        outfits = Outfit.query.get_or_404(id)  
        returned_data=[{
                'id': outfits.id,
                'sex': outfits.sex,
                'photo': outfits.photo,
                'description': outfits.description,
                'is_public': outfits.is_public,
                'genre_id': outfits.genre_id,
                'user_id': outfits.user_id
        }]        
    except:
        returned_data=[{'error':'error'}]
    return jsonify(returned_data)   


@api.route('/outfits/add', methods=['GET', 'POST'])
def add_outfit():
    add_outfit = True       
    returned_data = ""
    received_data = request.json
    try:
        outfit = Outfit(sex=received_data['sex'], photo=received_data['photo'], 
                        description=received_data['description'], 
                        is_public=received_data['is_public'],
                        genre_id=received_data['genre_id'],
                        user_id=received_data['user_id'])        
        db.session.add(outfit)
        db.session.commit()
        returned_data="Se creo un nuevo vestuario"
    except:
        returned_data="Hubo un error al crear vestuario"
    return returned_data

@api.route('/outfits/edit/<int:id>', methods=['GET', 'POST','PUT'])
def edit_outfit(id):
    add_outfit = False

    returned_data = ""
    received_data = request.json
    try:
        outfit = Outfit.query.get_or_404(id)    
        outfit.sex = received_data['sex']
        outfit.photo = received_data['photo']
        outfit.description = received_data['description']
        outfit.is_public=received_data['is_public']
        outfit.genre_id=received_data['genre_id']
        outfit.user_id=received_data['user_id']
        db.session.commit()            
        returned_data="Se edito un vestuario"
    except:
        returned_data="Hubo un error al editar vestuario"
    return returned_data



@api.route('/outfits/delete/<int:id>', methods=['GET', 'POST','DELETE'])
def delete_outfit(id):
    returned_data = ""
    try:
        outfit = Outfit.query.get_or_404(id)
        db.session.delete(outfit)
        db.session.commit()
        returned_data="Se elimino correctamente vestuario"
    except:
        returned_data="Hubo un error al eliminar vestuario"
    return returned_data



@api.route('/users', methods=['GET', 'POST'])
def list_users():
    users = User.query.all()
    tasks = []
    for x in users:
        tasks.append({
                'id': x.id,
                'email': x.email,
                'username': x.username,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'password_hash': x.password_hash,
                'is_admin': x.is_admin              
        })
    return jsonify(tasks)


@api.route('/users/show/<int:id>', methods=['GET', 'POST'])
def get_user(id):
    add_user = False
    returned_data = ""
    tasks = {}
    try:
        users = User.query.get_or_404(id)  
        returned_data=[{
                'id': users.id,
                'email': users.email,
                'username': users.username,
                'first_name': users.first_name,
                'last_name': users.last_name,
                'password_hash': users.password_hash,
                'is_admin': users.is_admin 
        }]        
    except:
        returned_data=[{'error':'error'}]
    return jsonify(returned_data)   


@api.route('/users/add', methods=['GET', 'POST'])
def add_user():
    add_user = True       
    returned_data = ""
    received_data = request.json
    try:
        user = User(email=received_data['email'], username=received_data['username'], 
                        first_name=received_data['first_name'], 
                        last_name=received_data['last_name'],
                        password=received_data['password_hash'],
                        is_admin=received_data['is_admin'])        
        db.session.add(user)
        db.session.commit()
        returned_data="Se creo un nuevo usuario"
    except:
        returned_data="Hubo un error al crear usuario"
    return returned_data


@api.route('/users/edit/<int:id>', methods=['GET', 'POST','PUT'])
def edit_user(id):
    add_user = False
    returned_data = ""
    received_data = request.json
    try:
        user = User.query.get_or_404(id)    
        user.email = received_data['email']
        user.username = received_data['username']
        user.first_name = received_data['first_name']
        user.last_name = received_data['last_name']
        user.password = received_data['password_hash']
        user.is_admin = received_data['is_admin']
        db.session.commit()            
        returned_data="Se edito un nuevo usuario"
    except:
        returned_data="Hubo un error al editar usuario"
    return returned_data

@api.route('/users/delete/<int:id>', methods=['GET', 'POST','DELETE'])
def delete_user(id):
    returned_data = ""
    try:
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        returned_data="Se elimino correctamente usuario"
    except:
        returned_data="Hubo un error al eliminar usuario"
    return returned_data 

@api.route('/users/login', methods=['GET', 'POST'])
def login():
    returned_data = ""
    j = request.json
    user = User.query.filter_by(email=j['email']).first()
    if user is not None and user.verify_password(j['password_hash']):
        returned_data = "validado"       
    else:
        returned_data = "no validado"
    return returned_data