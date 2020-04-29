from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    job = StringField('About job', validators=[DataRequired()])
    team_leader = StringField('Team leader id', validators=[DataRequired()])
    work_size = StringField('Time for job in hours', validators=[DataRequired()])
    collaborators = StringField("Collaborators' id", validators=[])
    is_finished = BooleanField('Is job ready?', validators=[])
    submit = SubmitField('Confirm')
