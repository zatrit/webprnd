from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ObtainTokenForm(FlaskForm):
    expires = SelectField("Истекает",
                          choices=[(0, "Никогда"),
                                   (2592000, "Через 30 дней"),
                                   (604800, "Через 7 дней"),
                                   (86400, "Через 1 день")])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Получить")