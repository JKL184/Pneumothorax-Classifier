from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField,HiddenField,SelectField,DateField,RadioField

from wtforms.validators import InputRequired, DataRequired,Email

class settingsForm(FlaskForm):
    size= IntegerField("Small Pneumothorax Size", validators=[DataRequired()])
    email = StringField('Email', validators=[InputRequired()])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
class searchForm(FlaskForm):
    identification=SelectField("identification", choices=["","Positive","Negative"], validators=[])
    patient= StringField("Patient Name",default="" ,validators=[])
    date= DateField("Date Scanned",default="",format='%d-%m-%Y')
    location = StringField('Location',default="", validators=[])
    employee = StringField('EmployeeID',default="", validators=[])
    
class resultsForm(FlaskForm):
    img=HiddenField("img", validators=[])
    confidence=HiddenField("confidence", validators=[])
    identification=HiddenField("identification", validators=[])
    patient= StringField("Patient Name", validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
class RegisterForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    lname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
