from datetime import datetime
from flask import render_template, redirect, url_for, flash, current_app, request
from flask_login import current_user, login_required
from app.main.forms import EditProfileForm
from app import db
from app.main import bp
from app.models import User


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    tektime= datetime.utcnow()
    if not current_user.is_authenticated:
        return render_template("index_anonymous.html", title='Home Page', tektime=tektime)
    return render_template("index.html", title='Home Page', tektime=tektime)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', title='Изменение данных аккаунта', form=form)


@bp.route('/about')
@login_required
def about():
    return render_template("about.html", title='About')
