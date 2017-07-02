# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import Genreform, Outfitform
from .. import db
from ..models import Genre, User, Outfit
from ..auth.forms import RegistrationForm


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
        db.session.add(outfit)
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

@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a user to the database
    """
    check_admin()

    add_user = True

    form = Userform()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                                description=form.description.data)
        try:
            # add user to the database
            db.session.add(user)
            db.session.commit()
            flash('You have successfully added a new user.')
        except:
            # in case user name already exists
            flash('Error: user name already exists.')

        # redirect to users page
        return redirect(url_for('admin.list_users'))

    # load user template
    return render_template('admin/user/user.html', action="Add",
                           add_user=add_user, form=form,
                           title="Add User")

@admin.route('/users/edit/<int:id>', methods=['GET', 'POST']) #/register
@login_required
def edit_user(id):
    """
    Editar usuario
    """
    check_admin()

    add_user = False

    user = User.query.get_or_404(id)
    form = RegistrationForm()
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
	user.first_name = form.first_name.data
	user.last_name = form.last_name.data
	user.password_hash = form.password_hash.data
	user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Se ha editado correctamente el usuario.')

        # redireccionando a la pagina de usuario 
        return redirect(url_for('admin.list_users'))

    form.email.data = user.email
    form.username.data = user.username
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
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
