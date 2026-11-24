from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contrasena', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contrasena', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, field):
        if User.get_by_username(field.data):
            raise ValidationError('Este nombre de usuario ya esta registrado.')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contrasena', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesion')
