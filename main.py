from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/works_log')
def func():
    session = db_session.create_session()
    job = session.query(Jobs)
    return render_template("jobs.html", job=job)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()
