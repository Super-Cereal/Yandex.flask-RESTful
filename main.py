from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.job_form import JobForm
from forms.departments_form import DepartmentsForm

from flask import Flask, render_template, redirect, abort, make_response, jsonify, url_for
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_restful import Api

from api import yandex_api, resourses_user, resourses_jobs

import requests
import os
# Логин и пароль Альбы Флорес - nairobi@mars.org  |  1234
# Логин и пароль Капитана - scott_shief@mars.org  |  1234


db_session.global_init('./db/one_db.sqlite')
app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
api.add_resource(resourses_user.UserListResourse, '/api/users')
api.add_resource(resourses_user.UserResourse, '/api/users/<int:user_id>')
api.add_resource(resourses_jobs.JobsListResourse, '/api/jobs')
api.add_resource(resourses_jobs.JobsResourse, '/api/jobs/<int:user_id>')
app.register_blueprint(yandex_api.blueprint)
log_manager = LoginManager()
log_manager.init_app(app)


@app.errorhandler(403)
def error403(error):
    return make_response(jsonify({'error': 'Not allowed'}), 403)


@app.errorhandler(404)
def error404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def error405(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


@log_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User.email).filter(User.email == form.email.data).first():
            return render_template('form_register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким email или login уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            hometown=form.hometown.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect("/login")
    else:
        return render_template('form_register.html', title='Регистрация',
                               form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('form_login.html', title='Авторизация',
                               message="Неправильный логин или пароль", form=form)
    else:
        return render_template('form_login.html', title='Авторизация',
                               form=form)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")


@app.route('/deluser/<int:user_id>')
def del_user(user_id):
    if not current_user.is_authenticated:
        abort(403)
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    elif current_user != user and current_user.id != 1:
        abort(403)
    session.delete(user)
    session.commit()
    return redirect('/users')


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    form = RegisterForm()
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404)
    elif not current_user.is_authenticated or (current_user != user and current_user.id != 1):
        abort(403)
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.age = form.age.data
        user.hometown = form.hometown.data
        user.email = form.email.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.set_password(form.password.data)
        session.commit()
        return redirect('/users')
    else:
        form.name.data = user.name
        form.surname.data = user.surname
        form.age.data = user.age
        form.hometown.data = user.hometown
        form.email.data = user.email
        form.position.data = user.position
        form.speciality.data = user.speciality
        form.address.data = user.address
        return render_template('form_register.html', title="Edit user", form=form)


@app.route('/users')
def users_table():
    session = db_session.create_session()
    users = session.query(User).all()
    return render_template("user_table.html", title="User table", users=users)


@app.route("/", methods=['GET', 'POST'])
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("jobs_table.html", title="Activity table", jobs=jobs)


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    if not current_user.is_authenticated:
        abort(403)
    form = JobForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        job = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data
        )
        session.add(job)
        session.commit()
        return redirect('/')
    else:
        return render_template('form_job.html', title='Adding a job', form=form)


@app.route("/addjob/<int:id>", methods=['GET', 'POST'])
def edit_job(id):
    form = JobForm()
    session = db_session.create_session()
    job = session.query(Jobs).get(id)
    if not job:
        abort(404)
    elif not current_user.is_authenticated or (current_user != job.user and current_user.id != 1):
        abort(403)
    if form.validate_on_submit():
        job.job = form.job.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        session.commit()
        return redirect('/')
    else:
        form.job.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
        return render_template('form_job.html', title='Editing a job', form=form)


@app.route('/deljob/<int:id>', methods=['GET', 'POST'])
def del_job(id):
    session = db_session.create_session()
    job = session.query(Jobs).get(id)
    if not job:
        abort(404)
    elif not current_user.is_authenticated or (current_user != job.user and current_user.id != 1):
        abort(403)
    session.delete(job)
    session.commit()
    return redirect('/')


@app.route('/departments', methods=['GET', 'POST'])
def departments():
    session = db_session.create_session()
    departments = session.query(Departments).all()
    return render_template('departments_table.html', title='Departments table',
                           departments=departments)


@app.route('/departments_add', methods=['GET', 'POST'])
def add_departments():
    if not current_user.is_authenticated:
        abort(403)
    form = DepartmentsForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        department = Departments(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
        )
        session.add(department)
        session.commit()
        return redirect('/departments')
    else:
        return render_template('form_departments.html', title='Adding a department', form=form)


@app.route("/departments_add/<int:id>", methods=['GET', 'POST'])
def edit_departments(id):
    if not current_user.is_authenticated:
        abort(403)
    form = DepartmentsForm()
    session = db_session.create_session()
    department = session.query(Departments).get(id)
    if not department:
        abort(404)
    elif current_user != department.user and current_user.id != 1:
        abort(403)
    if form.validate_on_submit():
        department.title = form.title.data
        department.chief = form.chief.data
        department.members = form.members.data
        department.email = form.email.data
        session.commit()
        return redirect('/departments')
    else:
        form.title.data = department.title
        form.chief.data = department.chief
        form.members.data = department.members
        form.email.data = department.email
        return render_template('form_departments.html', title='Editing a department', form=form)


@app.route('/departments_del/<int:id>', methods=['GET', 'POST'])
def del_departments(id):
    if not current_user.is_authenticated:
        abort(403)
    session = db_session.create_session()
    department = session.query(Departments).get(id)
    if not department:
        abort(404)
    elif current_user != department.user and current_user.id != 1:
        abort(403)
    session.delete(department)
    session.commit()
    return redirect('/departments')


@app.route('/home/<int:user_id>', methods=['GET'])
def users_show(user_id):
    user = requests.get(f'{url_for("index", _external=True)}/api/users/{user_id}').json()
    image = requests.get(f'{url_for("index", _external=True)}/api/yamaps/{user["users"][0]["hometown"]}').json()
    if 'error' in image:
        image = yandex_api.recode_image(open('static/img/none_image', 'rb'))
    return render_template('home.html', title='Homepage', image=image['image'], user=user["users"][0])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


'''
@app.before_first_request
@app.before_request
@app.after_request

'''
