from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField

from wtforms.validators import InputRequired, DataRequired,Email

class settingsForm(FlaskForm):

    size= IntegerField("Small Pneumothorax Size", validators=[DataRequired()])
    email = StringField('Email', validators=[InputRequired()])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

