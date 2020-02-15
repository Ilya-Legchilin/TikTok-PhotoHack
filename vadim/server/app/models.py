from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    role=db.Column(db.Integer)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    projects = db.relationship('Users_Projects', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(36))
    text = db.Column(db.String(140))
    posts = db.relationship('Post', backref='Father', lazy='dynamic')
    childrens = db.relationship('Users_Projects', backref='father', lazy='dynamic')
    def __repr__(self):
        return '<Project {} {} {} {}>'.format(self.id,self.name,self.text,self.posts)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1136))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    time = db.Column(db.DateTime)
    sosial_network=db.Column(db.String(136))
    topic=db.Column(db.String(136))
    text=db.Column(db.String(1036))
    media=db.Column(db.String(1036))
    status = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #один пользователь ко многим сообщениям
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
#ТО ЕСТЬ: Поле user_id было инициализировано как внешний ключ для user.id, что означает, что оно ссылается на значение id из таблицы users

    def __repr__(self):
        return '<Post id {}, project_id {}>'.format(self.body, self.project_id)

class Users_Projects(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
     project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
     asses = db.Column(db.Integer)

     def __repr__(self):
         return '<Project {} , project_id {}>'.format(self.id,self.project_id)
