from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, DateField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Чуваки, такой пользователь уже есть!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Чуваки, ваш е-мэйл говёный, введите иной')


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    about_me = TextAreaField('Обо мне', validators=[Length(min=0, max=140)])
    submit = SubmitField('Сохранить')


class EditPostForm(FlaskForm):

    #status = IntegerField()

    topic = StringField('Заголовок поста (если есть)')
    body = TextAreaField('тело поста',validators=[DataRequired()])
    network = StringField('Социальная сеть для которой предназначен пост')
    #time = DateField('Когда планируется к публикации')
    time =  DateField('планируется к публикации',
                          render_kw={'placeholder': '6/20/20 for June 20, 2020', 'type':'date'})
    submit = SubmitField('Отправить клиенту')
    toDraft = SubmitField('Сохранить в черновик')
    reLook = SubmitField('Предпросмотр')
