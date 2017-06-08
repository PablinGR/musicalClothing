# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import Generoform, Vestuarioform
from .. import db
from ..models import Genero, Usuario, Vestuario

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Genero Views

@admin.route('/generos', methods=['GET', 'POST'])
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

    form = Generoform()
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
        return redirect(url_for('admin.list_generos'))

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
        return redirect(url_for('admin.list_generos'))

    form.description.data = genero.description
    form.name.data = genero.name
    return render_template('admin/generos/genero.html', action="Edit",
                           add_genero=add_genero, form=form,
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


@admin.route('/generos/search', methods=['GET', 'POST'])
@login_required
def search_generos(id):

    check_admin()

    genero = Genero.query.get_or_404(id)
    form.description.data = genero.description
    form.name.data = genero.name
    return render_template('admin/generos/genero.html', add_vestuario=add_vestuario,
                           form=form, title="Buscar Vestuario")


# Vestuarios Views

@admin.route('/vestuarios', methods=['GET', 'POST'])
@login_required
def list_vestuarios():
    check_admin()
    vestuarios = Vestuario.query.all()
    return render_template('admin/vestuarios/vestuarios.html', vestuarios=vestuarios, title='Vestuario')


@admin.route('/vestuarios/add', methods=['GET', 'POST'])
@login_required
def add_vestuario():
    """
    Add a vestuario to the database
    """
    check_admin()

    add_vestuario = True

    form = VestuarioForm()
    if form.validate_on_submit():
        vestuario = Vestuario(sexo=form.sex.data,
                    foto=form.foto.data, genero_id=form.genero.data,
                    usuario_id=forms.usuario_id.data)

        try:
            # add vestuario to the database
            db.session.add(vestuario)
            db.session.commit()
            flash('You have successfully added a new vestuario.')
        except:
            # in case vestuario name already exists
            flash('Error: vestuario name already exists.')

        # redirect to the vestuarios page
        return redirect(url_for('admin.list_vestuarios'))

    # load vestuario template
    return render_template('admin/vestuarios/vestuarios.html', add_vestuario=add_vestuario,
                           form=form, title='Add Vestuario')


@admin.route('/vestuarios/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_vestuario(id):
    """
    Edit a vestuario
    """
    check_admin()

    add_vestuario = False

    vestuario = Vestuario.query.get_or_404(id)
    form = VestuarioForm(obj=vestuario)
    if form.validate_on_submit():
        vestuario.sexo=form.sex.data
        vestuario.foto=form.foto.data
        vestuario.genero_id=form.genero.data
        vestuario.usuario_id=form.usuario.data
        db.session.add(vestuario)
        db.session.commit()
        flash('You have successfully edited the vestuario.')

        # redirect to the vestuarios page
        return redirect(url_for('admin.list_vestuarios'))

    form.sex.data=vestuario.sexo
    form.foto.data=vestuario.fotos
    form.genero.data=vestuario.genero_id
    form.usuario.data=vestuario.usuario_id
    return render_template('admin/vestuarios/vestuario.html', search_genero=search_genero,
                           form=form, title="Edit Vestuario")

@admin.route('/vestuarios/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_vestuario(id):
    """
    Delete a vestuario from the database
    """
    check_admin()

    vestuario = Vestuario.query.get_or_404(id)
    db.session.delete(vestuario)
    db.session.commit()
    flash('You have successfully deleted the vestuario.')

    # redirect to the vestuarios page
    return redirect(url_for('admin.list_vestuarios'))

    return render_template(title="Delete Vestuario")


@admin.route('/vestuarios/search', methods=['GET', 'POST'])
@login_required
def search_vestuario(id):

    check_admin()

    vestuario = Vestuario.query.get_or_404(id)
    form.sex.data=vestuario.sexo
    form.foto.data=vestuario.foto
    form.genero.data=vestuario.genero_id
    form.usuario.data=vestuario.usuario_id
    return render_template('admin/vestuarios/vestuario.html', search_vestuario=search_vestuario_vestuario,
                           form=form, title="Buscar Vestuario")



# usuario edit view 
@admin.route('/admin/usuario/editUser', methods=['GET', 'POST'])
@login_required  
def editUser(): 
    """ 
    Handle requests to the /edit route 
    Edit an usuario to the database through the registration form 
    """ 
    form = RegistrationForm() 
    if form.validate_on_submit(): 
        usuario = Usuario(email=form.email.data, 
                            username=form.username.data, 
                            first_name=form.first_name.data, 
                            last_name=form.last_name.data, 
                            password=form.password.data) 
 
        # edit usuario to the database 
        db.session.merge(usuario)  
        db.session.commit() 
        flash('You have successfully registered! You may now login.') 
 
        # redirect to the login page 
        return redirect(url_for('auth.login')) 
 
    # load registration template 
    return render_template('auth/register.html', form=form, title='Register') 
 



