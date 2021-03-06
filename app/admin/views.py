# app/admin/views.py

import os

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from ..auth.forms import RegistrationForm
from forms import Genreform, Outfitform
from .. import db
from ..models import Genre, User, Outfit

from werkzeug import secure_filename

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Genre Views

@admin.route('/genres', methods=['GET', 'POST'])
@login_required
def list_genres():
    """
    List all genres
    """
    check_admin()

    genres = Genre.query.all()

    return render_template('admin/genre/genres.html',
                           genres=genres, title="Genres")

@admin.route('/genres/add', methods=['GET', 'POST'])
@login_required
def add_genre():
    """
    Add a genre to the database
    """
    check_admin()

    add_genre = True

    form = Genreform()
    if form.validate_on_submit():
        genre = Genre(name=form.name.data,
                                description=form.description.data)
        try:
            # add genre to the database
            db.session.add(genre)
            db.session.commit()
            flash('You have successfully added a new genre.')
        except:
            # in case genre name already exists
            flash('Error: genre name already exists.')

        # redirect to genres page
        return redirect(url_for('admin.list_genres'))

    # load genre template
    return render_template('admin/genre/genre.html', action="Add",
                           add_genre=add_genre, form=form,
                           title="Add Genre")

@admin.route('/genres/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_genre(id):
    """
    Edit a genre
    """
    check_admin()

    add_genre = False

    genre = Genre.query.get_or_404(id)
    form = Genreform(obj=genre)
    if form.validate_on_submit():
        genre.name = form.name.data
        genre.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the genre.')

        # redirect to the genres page
        return redirect(url_for('admin.list_genres'))

    form.description.data = genre.description
    form.name.data = genre.name
    return render_template('admin/genre/genre.html', action="Edit",
                           add_genre=add_genre, form=form,
                           genre=genre, title="Edit Genre")

@admin.route('/genres/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_genre(id):
    """
    Delete a genre from the database
    """
    check_admin()

    genre = Genre.query.get_or_404(id)
    db.session.delete(genre)
    db.session.commit()
    flash('You have successfully deleted the genre.')

    # redirect to the genres page
    return redirect(url_for('admin.list_genres'))

    return render_template(title="Delete Genre")


#Outfit Views

@admin.route('/outfits')
@login_required
def list_outfits():
    check_admin()
    
    outfits = Outfit.query.all()
    return render_template('admin/outfits/outfits.html', outfits=outfits, 
                            title='Outfits')

@admin.route('/outfits/add', methods=['GET', 'POST'])
@login_required
def add_outfit():
    check_admin()
    add_outfit = True

    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'outfits')

    form = Outfitform()
    if form.validate_on_submit():
        print(form.user.data)
        file = form.photo
        filename = os.path.join(IMAGES_DIR,secure_filename(form.photo.data.filename))

        outfit = Outfit(sex=form.sex.data, 
                        photo=filename, 
                        description=form.description.data, 
                        is_public=form.is_public.data,
                        genre_id=form.genre.data.id,
                        user_id=form.user.data.id
                        )
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
    form.user.data=outfit.user_id
    form.genre.data=outfit.genre_id
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
    del form.email
    del form.username
    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.password = form.password.data
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Se ha editado correctamente el usuario.')

        # redirect to the users page
        return redirect(url_for('admin.list_users'))
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
