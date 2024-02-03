from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(label='Имя пользователя', validators=[DataRequired(message='Заполните имя!')])
    password = PasswordField(label='Пароль', validators=[DataRequired(message='Заполните пароль!')])
    remember_me = BooleanField(label='Запомнить меня')
    submit = SubmitField(label='Далее')


class RegistrationForm(FlaskForm):
    username = StringField('Имя', validators=[DataRequired('Заполните имя')])
    email = StringField('Email', validators=[DataRequired('Заполните электронный адрес'), Email('Неверный синтаксис электронного адреса')])
    password = PasswordField('Пароль', validators=[DataRequired('Пароль не должен быть пустым')])
    password2 = PasswordField('Повтор пароля', validators=[DataRequired('Повторите пароль'), EqualTo('password', 'Пароли должны совпадать')])
    submit = SubmitField('Зарегистрировать')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такое имя уже занято')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Электронный адрес уже занят :(')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Адрес эл.почты', validators=[DataRequired('Заполните электронный адрес'), Email('Неверный синтаксис электронного адреса')])
    submit = SubmitField('Выслать инструкцию')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired('Пароль не должен быть пустым')])
    password2 = PasswordField('Повтор пароля', validators=[DataRequired('Повторите пароль'), EqualTo('password', 'Пароли должны совпадать')])
    submit = SubmitField('Обновить пароль')
