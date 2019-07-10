from flask_wtf import FlaskForm
from datetime import date
from wtforms import SubmitField, StringField, PasswordField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from app.models import User


class ReservarForm(FlaskForm):

    fecha = DateField("Fecha", format='%Y-%m-%d', validators=[DataRequired()])
    hour = StringField("Hora", validators=[DataRequired()])
    numero = StringField("Numero Sala", validators=[DataRequired()])
    submit = SubmitField("Reservar")


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):

    name = StringField("Nombre Completo", validators=[DataRequired()])
    telefono = StringField("Telefono", validators=[DataRequired()])
    email = StringField("Correo Electronico", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password1 = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Enviar")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Porfavor escoger otro username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Porfavor ingrese otro email")
