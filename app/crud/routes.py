import os
import datetime
import transliterate
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import current_user, login_required
from app import db
from werkzeug.utils import secure_filename
from app.crud.forms import UserForm, PageSiteForm, SiteFileForm
from app.crud import bp
from app.models import User, PageSite, SiteFile


@bp.route('/')
@login_required
def index():
    # if current_user.get_admin():
         return render_template('crud/crud.html', title='CRUD')
    # flash('У Вас нет доступа к администрированию!', 'danger')
    # return redirect(url_for('main.index'))


@bp.route('/<model_name>')
@login_required
def crud_list(model_name=None):
    models = ["User", "PageSite", "SiteFile"]
    if model_name not in models:
        flash(f'для таблицы {model_name} не предусмотрена GRUD', 'info')
        return redirect(url_for('crud.index'))
    model = globals()[model_name]
    rezult_query =model.query.all()
    return render_template(template_name_or_list=f'crud/table.html', title=model_name, list=rezult_query, model_name=model_name)


@bp.route('/<model_name>/add', methods=['GET', 'POST'])
@login_required
def add(model_name):
    dict_models = {"User": UserForm, "PageSite": PageSiteForm, "SiteFile": SiteFileForm}
    form = dict_models[model_name]()
    if form.validate_on_submit():
        if model_name == 'User':
            new_record = User(username=form.username.data, email=form.email.data, is_admin=form.is_admin.data)
        if model_name == 'PageSite':
            new_record = PageSite(title=form.title.data, name_route=form.name_route.data, page_body=form.page_body.data)
        if model_name == 'SiteFile':
            file = form.img.data
            s_filename = None
            if file:
                s_filename = secure_filename(transliterate.translit(file.filename, 'ru', reversed=True))
                file.save(os.path.join(current_app.config['UPLOAD_SAVE'], s_filename))
                new_record = SiteFile(filename=s_filename)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('crud.crud_list', model_name=model_name))
    return render_template('crud/add_edit.html', title='Добавление записи', form=form)


@bp.route('/<model_name>/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(model_name, id):
    models = ["User", "PageSite"]
    if model_name not in models:
        flash(f'для таблицы {model_name} не предусмотрена форма Редактирования', 'info')
        return redirect(url_for('crud.crud_list', model_name=model_name))

    model = globals()[model_name]
    record = model.query.get_or_404(id)

    form_models = {"User": UserForm, "PageSite": PageSiteForm}
    form = form_models[model_name](obj=record)

    template_name = 'crud/add_edit.html'

    if form.validate_on_submit():
        form.populate_obj(record)
        db.session.commit()
        return redirect(url_for('crud.crud_list', model_name=model_name))
    return render_template(template_name_or_list=template_name, title='Редактирование записи', form=form)


@bp.route('/<model_name>/del/<int:id>', methods=['POST'])
@login_required
def delete(model_name, id):
    model = globals()[model_name]
    record = model.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(record)
        db.session.commit()
    return redirect(url_for('crud.crud_list', model_name=model_name))


@bp.route('/<model_name>/upload', methods=['GET', 'POST'])
@login_required
def upload(model_name):
    models = ["PageSite"]
    if model_name not in models:
        flash(f'для таблицы {model_name} не предусмотрена загрузка из файла', 'info')
        return redirect(url_for('crud.crud_list', model_name=model_name))
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        file_data = file.read().decode("windows-1251")
        lines = file_data.split("\n")
        count = 0
        for line in lines:
            row = line.split(";")
            count += 1
            if line.count(';') >= 1 and count > 1:
                if model_name == 'PageSite':
                    title = row[0].strip()
                    name_route = row[1].strip()
                    page_body = row[2].strip()
                    yes_record = PageSite.query.filter(PageSite.name_route == name_route).first()
                if not yes_record:
                    if model_name == 'PageSite':
                        new_record = PageSite(title=title, name_route=name_route, page_body=page_body)
                        db.session.add(new_record)
                        db.session.commit()
                else:
                    yes_record.title = title
                    if model_name == 'PageSite':
                        yes_record.page_body = page_body
                        db.session.commit()
        return redirect(url_for('crud.crud_list', model_name=model_name))
    else:
        return render_template('crud/upload.html', title='Загрузка из csv-файла')


