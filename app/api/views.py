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

@admin.route('/outfits/add', methods=['GET', 'POST'])
@login_required
def add_outfit():
    check_admin()
    add_outfit = True

    form = Outfitform()
    if form.validate_on_submit():
        outfit = Outfit(sex=form.sex.data, photo=form.photo.data, 
                        description=form.description.data, 
                        is_public=form.is_public.data)
        try:
            db.session.add(outfit)
            db.session.commit()
            flash('You have successfully added a new outfit')
        except Exception as e:
            flash('Error')

        return redirect(url_for('admin.list_outfits'))

    return render_template('admin/outfits/outfit.html',action="Add",
                            add_outfit=add_outfit, form=form,
                            title="Add Outfit")


@admin.route('outfits/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_outfit(id):
    check_admin()
    add_outfit = False

    outfit = Outfit.query.get_or_404(id)
    form = Outfitform()
    if form.validate_on_submit():
        outfit.sex = form.sex.data
        outfit.photo = form.photo.data
        outfit.description = form.description.data
        outfit.is_public=form.is_public.data
        db.session.commit()
        flash('You have successfully edited the outfit')

        return redirect(url_for('admin.list_outfits'))

    form.sex.data=outfit.sex
    form.photo.data=outfit.photo
    form.description.data=outfit.description
    form.is_public.data=outfit.is_public
    return render_template('admin/outfits/outfit.html',action="Add",
                            add_outfit=add_outfit, form=form,
                            title="Edit Outfit")


@admin.route('outfits/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_outfit(id):
    check_admin()

    outfit = Outfit.query.get_or_404(id)
    db.session.delete(outfit)
    db.session.commit()
    flash('You have successfully deleted the outfit.')

    return redirect(url_for('admin.list_outfits'))

    return render_template(title="Delete Outfit")

# sin probar
# Outfit search

# @admin.route('/outfit/search/<string:genre>')
# @login_required
# def search_outfits(genre):
#     check_admin()
    
#     outfits = Outfit.query.filter_by(genre=genre).all()
#     return render_template('admin/outfits/outfits.html', outfits=outfits, 
#                             title='Outfits')


#sin probar
# User Views

@admin.route('/users', methods=['GET', 'POST'])
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()

    return render_template('admin/user/users.html',
                           users=users, title="Users")

@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    """
    Editar usuario
    """
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)
    form =RegistrationForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.password_hash = form.password.data
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Se ha editado correctamente el usuario.')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))

    form.email.data = user.email
    form.username.data=user.username
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.password.data = user.password_hash
    form.is_admin.data = user.is_admin
    return render_template('auth/register.html', action="Edit",
                           add_user=add_user, form=form,
                           user=user, title="Edit User")

@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user from the database
    """
    check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the users page
    return redirect(url_for('admin.list_users'))

    return render_template(title="Delete User")
