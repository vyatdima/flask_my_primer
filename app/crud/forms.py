from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed


class SiteFileForm(FlaskForm):
    img = FileField('Выберите файл', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class UserForm(FlaskForm):
    username = StringField('логин', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    new_password = StringField('Изменить пароль на')
    save_password = BooleanField('Сохранить пароль')
    is_admin = BooleanField('админ')
    submit = SubmitField('Сохранить')


class PageSiteForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    name_route = StringField('Маршрут', validators=[DataRequired()])
    page_body = TextAreaField('Содержимое страницы')
    submit = SubmitField('Сохранить')
