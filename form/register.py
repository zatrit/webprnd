from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[
                             DataRequired(), Length(min=8)])
    password_again = PasswordField(
        "Повторите пароль", validators=[EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")
