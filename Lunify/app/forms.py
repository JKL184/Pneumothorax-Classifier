from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, DataRequired, Email

class settingsForm(FlaskForm):

    size= IntegerField("Small Pneumothorax Size", validators=[DataRequired])
    email= EmailField("")