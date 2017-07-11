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
                'nombre': x.name,
                'descripcion': x.description        
              
        })
    return jsonify(tasks)

@api.route('/genres/show/<int:id>', methods=['GET', 'POST'])
def get_genre(id):
    store = False
    returned_data = ""
    tasks = {}
    try:
        genre = Genre.query.get_or_404(id)  
        returned_data=[{
                'id': genre.id,
                'nombre': genre.name,
                'descripcion': genre.description        
              
        }]
        
    except:
        returned_data=[{'error':'error'}]
    return jsonify(returned_data)   
            
    
    
@api.route('/genres/add', methods=['GET', 'POST'])
def add_genre():
    store = True    
    returned_data = ""
    received_data = request.json
    try:
        gen = Genre(name=received_data['name'],description=received_data['description'])
        db.session.add(gen)
        db.session.commit()
        returned_data="Se Creo una nueva data aleatoria"
    except:
        returned_data="Hubo un error"
    return returned_data

        
@api.route('/genres/edit/<int:id>', methods=['GET', 'POST', 'PUT'])
def edit_genre(id):
    store = False
    returned_data = ""
    received_data = request.json
    try:
        genre = Genre.query.get_or_404(id)    
        genre.name = received_data['name']
        genre.description = received_data['description']
        db.session.commit()            
        returned_data="Se edito un dato"
    except:
        returned_data="Hubo un error al editar"
    return returned_data

@api.route('/genres/delete/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete_genre(id):
    returned_data = ""
    try:
        genre = Genre.query.get_or_404(id)
        db.session.delete(genre)
        db.session.commit()
        returned_data="Se elimino correctamente"
    except:
        returned_data="Hubo un error al eliminar"
    return returned_data
        

@api.route('/outfits', methods=['GET', 'POST'])
def list_outfits():
    outfits = Outfit.query.all()
    tasks = []
    for x in outfits:
        tasks.append({
                'id': x.id,
                'sexo': x.sex,
                'foto': x.photo,
                'descripcion': x.description,
                'is_public': x.is_public,
                'genre_id': x.genre_id,
                'user_id': x.user_id              
        })
    return jsonify(tasks)

