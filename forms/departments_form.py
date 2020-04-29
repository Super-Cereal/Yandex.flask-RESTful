from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired, Email


class DepartmentsForm(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief = StringField("Cheief's id", validators=[DataRequired()])
    members = StringField("Members' id", validators=[DataRequired()])
    email = StringField("Department email", validators=[DataRequired(), Email()])
    submit = SubmitField("Confirm")
