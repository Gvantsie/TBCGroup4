from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import StringField, PasswordField, DateField, RadioField, SelectField, SubmitField, FloatField
from wtforms.validators import DataRequired, length, equal_to

from choices import COUNTRIES


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანეთ თქვენი იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("შექმენით პაროლი", validators=[DataRequired(), length(min=8, max=64)])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[DataRequired(), equal_to("password")])

    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()

    login = SubmitField("შესვლა")


class ProductForm(FlaskForm):
    img = FileField("ატვურთეთ პროდუქტის ფოტო:")
    name = StringField("პროდუქტის სახელი")
    price = FloatField("პროდუქტის ფასი")

    submit = SubmitField("პროდუქტის შექმნა")

class CommentForm(FlaskForm):
    text =  StringField("დაწერეთ კომენტარი")
    submit = SubmitField("დაწერა")

