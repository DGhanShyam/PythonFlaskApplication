from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm1(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), Length(min=2, max= 25)])
    password= PasswordField('Password', validators=[DataRequired(), Length(min=5, max= 25)])
    confirm_pass= PasswordField('Confirm_Password', validators=[DataRequired(),
                                                     EqualTo('password')])
    email= PasswordField('Email', validators=[DataRequired(), Email() ])                                                 
    submit= SubmitField('Sign Up')

class LoginForm1(FlaskForm):
    email= PasswordField('Email', validators=[DataRequired(), Email() ])                                                 
    password= PasswordField('Password', validators=[DataRequired(), Length(min=5, max= 20)])

    submit= SubmitField('Sign Up')    