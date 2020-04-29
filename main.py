from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
from forms.job_form import JobForm
from forms.departments_form import DepartmentsForm

from flask import Flask, render_template, redirect, abort, make_response, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_restful import Api

from api import yandex_api, resourses_user, resourses_jobs

import requests
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
        if session.query(User.email).filter(User.email == form.login_or_email.data).first():
            return render_template('form_register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким email или login уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login_or_email.data,
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


@app.route("/", methods=['GET', 'POST'])
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template("jobs_table.html", title="Activity table",
                           current_user=current_user,
                           jobs=jobs)


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


@app.route('/users_show/<int:user_id>', methods=['GET'])
def users_show(user_id):
    user = requests.get(f'http://127.0.0.1:8000/api/users/{user_id}').json()
    if 'error' in user:
        return f'<h1 style="text-align: center">error: {user["error"]}</h1>'

    image = requests.get(f'http://127.0.0.1:8000/api/yamaps/{user["hometown"]}').json()
    if 'error' in image:
        return f'<h1 style="text-align: center">{image["error"]}</h1>'
    return render_template('image_hometown.html', image=image['image'], user=user)


if __name__ == "__main__":
    app.run(port=8000)


'''
@app.before_first_request
@app.before_request
@app.after_request

'''
