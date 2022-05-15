from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField

from wtforms.validators import InputRequired, DataRequired,Email

class settingsForm(FlaskForm):
    size= IntegerField("Small Pneumothorax Size", validators=[DataRequired()])
    email = StringField('Email', validators=[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

<<<<<<< HEAD
class resultsForm(FlaskForm):
    patient= StringField("Patient Name", validators=[DataRequired()])
    location = StringField('Location', validators=[InputRequired()])
    employee = StringField('EmployeeID', validators=[InputRequired()])
=======
class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
>>>>>>> da9745670bb9be0e51fe045884fd60f5c1f0c254
