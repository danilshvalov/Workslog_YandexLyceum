from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class AddWork(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField("id тимлида", validators=[DataRequired()])
    work_size = IntegerField("Продолжительность в часах", validators=[DataRequired()])
    collaborators = StringField("Список id команды", validators=[DataRequired()])
    is_finished = BooleanField('Работа завершена?')
    submit = SubmitField('Применить')