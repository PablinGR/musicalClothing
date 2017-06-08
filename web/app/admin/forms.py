# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..models import Usuario, Genero

class Generoform(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')



class Vestuarioform(FlaskForm):

	sex = SelectField(u'Sexo', choices=[('H', 'Hombre'), ('M', 'Mujer')], validators=[DataRequired()])
	foto = StringField('Foto', validators=[DataRequired()])
	genero = QuerySelectField(query_factor=lambda: Genero.query.all(), get_label="name", validators=[DataRequired()])
	usuario = QuerySelectField(query_factor=lambda: Usuario.query.all(), get_label="username", validators=[DataRequired()])
	submit = SubmitField('Submit')
