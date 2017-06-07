# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import GeneroForm
from .. import db
from ..models import Genero

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Genero Views

@admin.route('/genero', methods=['GET', 'POST'])
@login_required
def list_generos():
    """
    List all generos
    """
    check_admin()

    generos = Genero.query.all()

    return render_template('admin/generos/generos.html',
                           generos=generos, title="Generos")

@admin.route('/generos/add', methods=['GET', 'POST'])
@login_required
def add_genero():
    """
    Add a genero to the database
    """
    check_admin()

    add_genero = True

    form = GeneroForm()
    if form.validate_on_submit():
        genero = Genero(name=form.name.data,
                                description=form.description.data)
        try:
            # add genero to the database
            db.session.add(genero)
            db.session.commit()
            flash('You have successfully added a new genero.')
        except:
            # in case genero name already exists
            flash('Error: genero name already exists.')

        # redirect to generos page
        return redirect(url_for('admin.list_departments'))

    # load genero template
    return render_template('admin/generos/genero.html', action="Add",
                           add_genero=add_genero, form=form,
                           title="Add Genero")

@admin.route('/generos/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_genero(id):
    """
    Edit a genero
    """
    check_admin()

    add_genero = False

    genero = Genero.query.get_or_404(id)
    form = Generoform(obj=genero)
    if form.validate_on_submit():
        genero.name = form.name.data
        genero.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the genero.')

        # redirect to the generos page
        return redirect(url_for('admin.list_departments'))

    form.description.data = genero.description
    form.name.data = genero.name
    return render_template('admin/generos/genero.html', action="Edit",
                           add_genero=add_department, form=form,
                           genero=genero, title="Edit Genero")

@admin.route('/generos/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_genero(id):
    """
    Delete a genero from the database
    """
    check_admin()

    genero = Genero.query.get_or_404(id)
    db.session.delete(genero)
    db.session.commit()
    flash('You have successfully deleted the genero.')

    # redirect to the generos page
    return redirect(url_for('admin.list_generos'))

    return render_template(title="Delete Genero")