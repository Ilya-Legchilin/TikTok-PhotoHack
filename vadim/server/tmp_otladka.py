from app import app, db
from app.models import User, Post

u = User.query.all()
p = Post.query.all()
p

for i in p:
    db.session.delete(i)

db.session.commit()





for i in u:
    db.session.delete(i)

db.session.commit()


import datetime
k=0
kk=-1
for i in range(60):
    k+=1
    kk+=1
    pp=Post(sosial_network='facebook', topic='Загаловок'+str(i), body='тело поста #' + str(i), status=k, user_id=1, project_id=2, time=datetime.datetime(2020,10,12,18,41,39,162847), text='По рзелульаттам илссеовадний одонго анлигйсокго унвиертисета, не иеемт занчнеия, в кокам пряокде рсапожолены бкувы в солве. Галвоне, чотбы преавя и пслоендяя бквуы блыи на мсете. Осатьлыне бкувы мгоут селдовтаь в плоонм бсепордяке, все-рвано ткест ... кдаужю бкуву по отдльенотси, а все солво?'+str(k)) 
    if k==6:
        k=0
    if kk==2:
        kk=0
    db.session.add(pp)

db.session.commit()
