from quart_wtf import QuartForm, FileRequired
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FileField
)
from wtforms.validators import DataRequired, Email, Length


class SearchFrom(QuartForm):
    search_input = StringField('searchInput', validators=[DataRequired()], render_kw={"class": "form-control me-2",
                                                                                 "placeholder": "Поиск"})
    submit = SubmitField('Поиск', render_kw={"class": "btn btn-outline-success"})

class UploadFile(QuartForm):
    file = FileField(validators=[FileRequired()], render_kw={"id": "image-upload",
                                                             "class": "btn btn-primary form-control"})
    titleCard = StringField('titleCard', validators=[DataRequired()], render_kw={"class": "form-control mt-3 mb-3",
                                                                                 "placeholder": "Название карточки"})

    hashTag = StringField('HashTag', validators=[DataRequired()], render_kw={"class": "form-control mt-3 mb-3",
                                                                                 "placeholder": "тег для поиска"})

    submit = SubmitField('Добавить', render_kw={"class": "btn btn-primary form-control"})


class UserRegistration(QuartForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control",
                                                                                  "placeholder": "Почта"})
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)], render_kw={"class": "form"
                                                                                                                "-control",
                                                                                                       "placeholder": "Имя"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control",
                                                                                 "placeholder": "Пароль"})
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary"})


class LoginAuto(QuartForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control",
                                                                                  "placeholder": "Почта"})

    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control",
                                                                                 "placeholder": "Пароль"})
    submit = SubmitField('Авторизоваться', render_kw={"class": "btn btn-primary"})
