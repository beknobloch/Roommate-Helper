from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DecimalField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
        Regexp(r'.*\d.*', message="Password must contain at least one number."),
        Regexp(r'.*[A-Z].*', message="Password must contain at least one uppercase letter."),
        Regexp(r'.*[a-z].*', message="Password must contain at least one lowercase letter."),
        Regexp(r'.*[!@#$%^&*()-_=+<>?/].*', message="Password must contain at least one special character (example: !@#$%^&*).")
    ])
    balance = FloatField('Balance', validators=[NumberRange(min=0, message="Balance must be non-negative.")])
    submit = SubmitField('Register')

class LogoutForm(FlaskForm):
    submit = SubmitField('Logout')
