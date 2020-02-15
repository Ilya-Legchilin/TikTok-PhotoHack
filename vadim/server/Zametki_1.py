from app import app, db
from app.models import User, Post




for i in range(10):
    p=Post(sosial_network='facebook', topic=str(i)+' Загаловок', body='текст поста #' + str(i), status=i, user_id=i)
    db.session.add(p)
    db.session.commit()
