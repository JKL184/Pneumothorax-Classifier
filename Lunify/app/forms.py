from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField

from wtforms.validators import InputRequired, DataRequired,Email

class settingsForm(FlaskForm):

    size= IntegerField("Small Pneumothorax Size", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
