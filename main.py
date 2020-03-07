from flask import Flask, render_template, redirect, request, abort
from flask_login import login_user
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime
from flask_login import LoginManager, login_required, logout_user, current_user
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.add_work_form import AddWork

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def base():
    return render_template('base.html', title='Home')


@app.route('/works_log')
def func():
    session = db_session.create_session()
    job = session.query(Jobs)
    return render_template("jobs.html", job=job)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.email = form.email.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/works_log")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_work', methods=['GET', 'POST'])
@login_required
def add_work():
    form = AddWork()
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = current_user.id
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        current_user.jobs.append(jobs)
        session.merge(current_user)
        session.commit()
        return redirect('/works_log')
    return render_template('add_work.html', title='Добавление работы', form=form)


@app.route('/works_log/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_works_log(id):
    form = AddWork()
    if request.method == "GET":
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id, ((Jobs.team_leader == current_user.id) |
                                                          (current_user.id == 1))).first()
        if jobs:
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        session = db_session.create_session()
        jobs = session.query(Jobs).filter(Jobs.id == id, ((Jobs.team_leader == current_user.id) |
                                                          (current_user.id == 1))).first()
        if jobs:
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            session.commit()
            return redirect('/works_log')
        else:
            abort(404)
    return render_template('add_work.html', title='Редактирование новости', form=form)


@app.route('/works_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def works_delete(id):
    session = db_session.create_session()
    jobs = session.query(Jobs).filter(Jobs.id == id, ((Jobs.team_leader == current_user.id) |
                                                      (current_user.id == 1))).first()
    if jobs:
        session.delete(jobs)
        session.commit()
    else:
        abort(404)
    return redirect('/works_log')


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
