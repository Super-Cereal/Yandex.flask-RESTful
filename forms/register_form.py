from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    email = StringField('Login/email', validators=[DataRequired('Поле должно быть заполнено'),
                                                            Email('Некоректный email')])
    password = PasswordField('Password', validators=[DataRequired('Поле должно быть заполнено')])
    password_again = PasswordField('Repeat password', validators=[DataRequired('Поле должно быть заполнено'),
                                                                  EqualTo('password', 'Пароли не совпадают')])
    surname = StringField('Surname', validators=[DataRequired('Поле должно быть заполнено')])
    name = StringField('Name', validators=[DataRequired('Поле должно быть заполнено')])
    age = StringField('Age', validators=[DataRequired('Поле должно быть заполнено')])
    hometown = StringField('Hometown', validators=[DataRequired('Поле должно быть заполнено')])
    position = StringField('Position', validators=[DataRequired('Поле должно быть заполнено')])
    speciality = StringField('Spesiality', validators=[DataRequired('Поле должно быть заполнено')])
    address = StringField('Address', validators=[DataRequired('Поле должно быть заполнено')])
    submit = SubmitField('Submit')
