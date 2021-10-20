from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Email,EqualTo,NumberRange
from wtforms import StringField,PasswordField,SubmitField
from wtforms import ValidationError
class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login!')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('confir_password',message='Password Must Match')])
    confir_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def check_email(self,email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email Has Been Registered')

    def check_Username(self,username):
        if User.query.filter_by(email=self.username.data).first():
            raise ValidationError('username Has Been Registered')


