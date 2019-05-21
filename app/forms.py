from wtforms import StringField, PasswordField, \
    SubmitField, BooleanField, SelectField, HiddenField, validators, ValidationError, TextAreaField
from flask_wtf import FlaskForm
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(4, 30, "Invalid Length")])
    confirm = PasswordField('Confirm', [
        validators.DataRequired(),
        validators.EqualTo('password', 'Passwords must match')
    ])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Register')
    #hidden_tag = HiddenField('Hidden')

    def validate_email(self, email):
        print("verifying...")
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("The user with such email already exists.")

    def validate_username(self, username):
        print("verifying...")
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("The user with such username already exists.")


class EditProfileForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    about_me = TextAreaField('About me', [validators.Length(min=0, max=140)])
    submit = SubmitField('Submit')
