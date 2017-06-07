# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class GeneroForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    submit = SubmitField('Submit')