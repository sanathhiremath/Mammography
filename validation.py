from flask_wtf import FlaskForm
from wtforms import  SubmitField, TextAreaField,Form, BooleanField, StringField, PasswordField, validators, TextField
from wtforms.validators import DataRequired, Email, InputRequired, Length


class DoctorRegistrationForm(FlaskForm):
    #d=json.loads(FlaskForm)
    name = TextField('Name', validators=[validators.required()])
    dob=TextField('Date of Birth', validators=[validators.required()])
    phonenumber=TextField('Phone Number', validators=[validators.required()])
    specialization=TextField('Specialization', validators=[validators.required()])
    email = TextField('Email', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password', validators=[validators.required(), validators.Length(min=3, max=35)])
