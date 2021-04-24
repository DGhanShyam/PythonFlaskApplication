from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username= StringField('Username', validators=[DataRequired(), Length(min=2, max= 25)])
    password= PasswordField('Password', validators=[DataRequired(), Length(min=3, max= 25)])
    confirm_pass= PasswordField('Confirm_Password', validators=[DataRequired(),
                                                     EqualTo('password')])
    email= PasswordField('Email', validators=[DataRequired(), Email() ]) 

    radio_button = RadioField("", choices=[('ON', 'ON'), ('OFF', 'OFF'), ('Not Used', 'False')])
    bhk = SelectField('BHK', [DataRequired()],
                        choices=[('1', '1 BHK'),
                                 ('2', '2 BHK'),
                                 ('3', '3 BHK'),
                                 ('4', '4 BHK'),    ])                    

    address= StringField('Address', validators=[DataRequired(), Length(min=2, max= 45)])
    pincode= StringField('Pincode', validators=[DataRequired(), Length(min=2, max= 25)])
    city= StringField('City', validators=[DataRequired(), Length(min=2, max= 30)])
    state= StringField('State', validators=[DataRequired(), Length(min=2, max= 30)]) 
    phone_no= StringField('Phone_Number', validators=[DataRequired(), Length(min=2, max= 14)]) 

    submit= SubmitField('Sign Up')
    submit1= SubmitField('Search')


class LoginForm(FlaskForm):
    email= PasswordField('Email', validators=[DataRequired(), Email() ])                                                 
    password= PasswordField('Password', validators=[DataRequired(), Length(min=5, max= 20)])

    submit= SubmitField('Sign Up')    

class Home_input(FlaskForm):
    bhk = SelectField('BHK', [DataRequired()],
                        choices=[('1', '1 BHK'),
                                 ('2', '2 BHK'),
                                 ('3', '3 BHK'),
                                 ('4', '4 BHK'),                                                                                                                   
                                                ])                    

    address= StringField('Address', validators=[DataRequired(), Length(min=2, max= 45)])
    pincode= StringField('Pincode', validators=[DataRequired(), Length(min=2, max= 25)])
    city= StringField('City', validators=[DataRequired(), Length(min=2, max= 25)])
    state= StringField('State', validators=[DataRequired(), Length(min=2, max= 25)])
    submit= SubmitField('Sign Up')

