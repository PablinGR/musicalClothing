# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import User, Genre

class Genreform(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Outfitform(FlaskForm):
    sex = SelectField(u'Sex', choices=[('M', 'Male'), ('F', 'Female')])
    photo = StringField('Photo', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    is_public = BooleanField('Public', validators=[DataRequired()])
    user = QuerySelectField(query_factory=lambda: User.query.all(), get_label="username")
    genre = QuerySelectField(query_factory=lambda: Genre.query.all(), get_label="name")
    submit = SubmitField('Submit')
