# -*- coding: utf-8 -*-
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, EditPostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post,Users_Projects,Project
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm
from datetime import datetime
from app.forms import EditProfileForm
import json
from functools import wraps
import os
import urllib.request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['jpg', 'pdf', 'png', 'mp4', 'jpeg', 'gif'])
IMAGE_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])
VIDEO_EXTENSIONS = set(['mp4'])

def allowed_file(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)

def is_image(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS)

def is_video(filename):
    return ('.' in filename and filename.rsplit('.', 1)[1].lower() in VIDEO_EXTENSIONS)

def get_type(filename):
    if is_image(filename):
        return 'i'
    if is_video(filename):
        return 'v'
    return '?'

@app.route('/upload', methods=['POST'])
def upload_file(post_id, project):
    print('post')
    print(os.getcwd())
    files_dict = {}
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
        files = request.files.getlist('files[]')
        i = 0
        v = 0
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                type = get_type(filename)
                directory = os.path.join(app.config['UPLOAD_FOLDER'], str(project), str(post_id))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                if (type == 'i'):
                    i += 1
                    files_dict.update({type + str(i) : filename})
                    file.save(os.path.join(directory, filename))
                if (type == 'v'):
                    v += 1
                    files_dict.update({type + str(v) : filename})
                    file.save(os.path.join(directory, filename))

        flash('File(s) successfully uploaded')
    return files_dict

def post_pageStatus(x):
    return {
        1 : 'posts_client/_post.html',
        2 : 'posts_client/_postDorab.html',
        3 : 'posts_client/_postCanceled.html',
        4 : 'posts_client/_postPlaned.html',
        5 : 'posts_client/_postPublished.html',
        6 : 'posts_client/_postDraft.html'
    }.get(x, 99)

def get_list_of_post_dicts(all_posts):
    posts_list = []
    for post in all_posts:
        posts_list.append({
            'ID'             : post.id,
            'BODY'           : post.body,
            'TIME_BORN'      : str(post.timestamp),
            'SOCIAL_NETWORK' : post.sosial_network,
            'USER_ID'        : post.user_id,
            'STATUS'         : post.status,
            'COMENT'         : post.text,
            'TIME'           : str(post.time),
            'TOPIC'          : post.topic,
            'PROJECT_ID'     : post.project_id,
            'MEDIA'          : post.media})
    return posts_list
# def client_or_spec(f):
# @wraps(f)
# def wrap(*args, **kwargs):
#     if current_user.role == 1:
#         return f(*args, **kwargs)
#     else:
#         flash("Вы не являетесь администратором, сорян!")
#         return redirect(url_for('index'))
#
#     return wrap

#return redirect(url_for('index'))

def requires_spec(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.role!=1:
            flash("Вы не являетесь администратором, сорян!")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapped

def owner_required(f):
    @wraps(f)
    def wrapped(**arg):
        if (arg['project'] != 'first'):
            User_projects_list = Users_Projects.query.filter_by(user_id=current_user.id).all()
            i = 0
            l = len(User_projects_list)
            print(l, 'AXAXAXAXA\n')
            while ((i < l) and (User_projects_list[i].project_id != int(arg['project']))):
                print(i, 'IIIIIIIIII')
                i += 1
            if (i == l):
                return redirect(url_for('index'))
            else:
                return f(**arg)

        else:
            return f(**arg)
    return wrapped

def requires_client(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if current_user.role!=0:
            flash("Вы не являетесь нашим клиентом, сорян!")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapped

@app.errorhandler(413)
def err_413(error):
    return 'OOPS! lage file'

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'neo36'}
    posts = [
        {
            'author': {'username': 'Сбербанк'},
            'body': 'Умение смеяться над собой не всегда работает в SMM. Пример «Сбербанка» это доказывает.'
        },
        {
            'author': {'username': 'Facebook'},
            'body': 'Качество аудитории имеет значение!'
        },
        {
            'author': {'username': 'Twitter'},
            'body': 'Скажите, кто тебя фоловит, и я скажу, кто ты!'
        }
    ]
    return render_template("index.html", title='диспетчер', posts=posts)
    #return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход к диспетчеру', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравлялки! Теперь вы зарегистрировались в КатяГраме!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Ты чувствуешь улучшение жизни? Нет? И я нет! А оно есть!'},
        {'author': user, 'body': 'Если вы пару раз дадите человеку взаймы, то он уже постоянно будет учитывать вас при планировании своих доходов.'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/projects/<project>', methods=['GET'])
@login_required
@owner_required
def projects(project,filter=None,quantity=None):
    print("зашли в проект: ", project)
    filter = request.args.get('filter', None)
    quantity = request.args.get('quantity', None) #количество
    print('фильтр такой', filter, 'а их количество:', quantity)
    try:
        if filter != None:
            filter=int(filter)
        else:
            filter=1
        if quantity != None:
            quantity=int(quantity)
    except ValueError:
        print('не верный формат get запроса')
    except BufferError:
        print('переполнение буфера')
    except RuntimeError:
        print('по моему кто-то пытается нас хакнуть')

    Projects_of_current_user_list=[]
    User_projects_list = Users_Projects.query.filter_by(user_id=current_user.id).all()

    #print(User_projects_list)

    for iter_project in User_projects_list:
        tmp = Project.query.filter_by(id=iter_project.project_id).first()
        Projects_of_current_user_list.append({'name' : tmp.name, 'id' : tmp.id})
    print(len(User_projects_list))
    if len(User_projects_list)>0 and project=='first':
        project = User_projects_list[0].project_id
    all_posts = []
    if (len(User_projects_list) != 0) and project=='first':
        project = User_projects_list[0].project_id
    if len(User_projects_list)==0:
        print('This user hasn\'t got projects')
        project = -1
    elif filter!=None:
        if (project != 'first'):
            all_posts = Post.query.filter_by(project_id=int(project), status=filter).all()
    else:
        if (project != 'first'):
            all_posts = Post.query.filter_by(project_id=int(project)).all()

    posts_list = get_list_of_post_dicts(all_posts)

    if quantity!=None:
        posts_list=posts_list[0:quantity]
    print('количество постов должно быть',quantity,'итак.. пересчёт:',len(posts_list))
    print(post_pageStatus(filter),type(post_pageStatus(filter)))

    print('\n\n\n')
    print(Projects_of_current_user_list)
    print()
    print(project)
    print('\n\n\n')

    return render_template('project.html', user=current_user, Posts=posts_list, Projects=Projects_of_current_user_list, current_project=int(project), filter=filter, post_str=post_pageStatus(filter))




@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Ваши изменения будут сохранены!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Редактировать профиль', form=form)


@app.route('/chagestatus', methods=['GET', 'POST'])
@login_required
def changestatus():
    print('дернули за ручку смены статуса')
    if request.method == "POST":
        post_id = request.form['id_post']
        set_status = request.form['set_status']

        print('post id is',post_id,'& his status will be ',set_status)
        try:
            the_post=Post.query.filter_by(id=int(post_id)).first()
            the_post.status = int(set_status)
            db.session.add(the_post)
            db.session.commit()
        except ValueError:
            print('не тот тип данных прилетел в json')
        except BufferError:
            print('метод переполнения буфера проходили. гуляй')
        except RuntimeError:
            print('по моему кто-то пытается нас хакнуть')


        conf_answer={'updated_id': post_id}
    return json.dumps(conf_answer)

@app.route('/givePosts', methods=['GET', 'POST'])
@login_required
def givePosts():
    print('ручка выдаст пост при правильном запросе')
    start_post = request.form['start_post']
    quantity = request.form['quantity']
    status_q = request.form['status']
    project = request.form['project']
    print(quantity,status_q,project,start_post)

    Projects_of_current_user_list=[]
    User_projects_list = Users_Projects.query.filter_by(user_id=current_user.id, asses=1).all()

    posts_list = []

    try:
        for iter_project in User_projects_list:
            tmp = Project.query.filter_by(id=iter_project.project_id).first()
            Projects_of_current_user_list.append({'name' : tmp.name, 'id' : tmp.id})


        if User_projects_list==None:
            print('This user hasn\'t got projects!')
        else:
            all_posts = Post.query.filter_by(project_id=int(project),status=int(status_q)).all()

        for post in all_posts:
            if post.id>=int(start_post):
                posts_list.append({
                    'ID'            : post.id,
                    'BODY'          : post.body,
                    'TIME'          : str(post.timestamp),
                    'SOCIAL_NETWORK': post.sosial_network,
                    'USER_ID'       : post.user_id})
    except ValueError:
        print('не тот тип данных прилетел в json')
    except BufferError:
        print('метод переполнения буфера проходили. гуляй')
    except RuntimeError:
        print('по моему кто-то пытается нас хакнуть')

    print(json.dumps(posts_list))
    return json.dumps(posts_list)

@app.route('/preview', methods=['POST', 'GET'])
#requires_spec
def post_preview():
    post_id = request.args.get('post_id', None)
    project = request.args.get('project', None)
    print(post_id, 'ABC\nABC\n')
    post_obj = Post.query.filter_by(id=int(post_id)).first_or_404()
    post = {
        'BODY'           : post_obj.body,
        'SOCIAL_NETWORK' : post_obj.sosial_network,
        'STATUS'         : post_obj.status,
        'TIME'           : str(post_obj.time),
        'TOPIC'          : post_obj.topic }

    return render_template('post_preview.html', post=post, project=project)

@app.route('/commentPost', methods=['GET', 'POST'])
@login_required
#@requires_client
def commentPost():
    print('ручка выдаст пост при правильном запросе')
    id_post = request.form['id_post']
    comment = request.form['comment']

    tmp_dump=0
    print(id_post, comment)

    try:
        post = Post.query.filter_by(id=int(id_post)).first_or_404()
        #print(post.text)
        post.text=str(comment)
        #Post(sosial_network='facebook', topic='Загаловок'+str(i), body='тело поста #' + str(i), status=k, user_id=1, project_id=2)
        #По-моему не надо вызывать адд. Я при редактировании не вызываю. Возможно будет создаваться новый пост
        db.session.add(post)
        db.session.commit()
        tmp_dump=1
    except ValueError:
        print('не тот тип данных прилетел в json')
    except BufferError:
        print('метод переполнения буфера проходили. гуляй')
    except RuntimeError:
        print('по моему кто-то пытается нас хакнуть')
    result={'result':1}
    return json.dumps(result)

def add_post_to_db(project, topic, body, network, time, status, id=None, media=None):
    print(topic,body,network,time,status, media)
    print('WvWvWvWvW\n', media, '\nWvWvWvWvW')
    #ОБРАБОТКА ИСКЛЮЧЕНИЙ!!!!!!!!!
    post_media = {'ui' : current_user.id, 'pr': int(project), 'pi' : -1}
    try:
        print("--------------------------")
        if (id):
            post_media['pi'] = id
            post_media.update(media)
            the_post=Post.query.filter_by(id=int(id)).first()
            the_post.sosial_network=network
            the_post.topic = topic
            the_post.body=body
            the_post.status=status
            the_post.user_id=current_user.id
            the_post.project_id=int(project)
            the_post.time=time
            the_post.media = str(post_media)
            db.session.commit()
            post_media['pi'] = the_post.id
            the_post.media = str(post_media)
            db.session.commit()
            print(the_post.id, 'id is there')
        else:
            print('\n\n\n\n\nXXXXXXXXXXXX3X', id)
            the_post=Post(sosial_network=network, topic=topic, body=body, status=status, user_id=current_user.id, project_id=int(project), time=time)
            db.session.add(the_post)
            db.session.commit()
            filenames_dict = upload_file(the_post.id, project)
            post_media['pi'] = the_post.id
            post_media.update(filenames_dict)
            the_post.media = str(post_media)
            db.session.commit()
            print(the_post.id, 'id is there')
        return the_post.id
        #return redirect(url_for('spec_projects', project=int(project), filter=1, quantity=5)
    except ValueError:
        print('не тот тип данных прилетел в json')
        return redirect(url_for('edit_post', post_id=int(the_post.id), project=int(project)))
    except BufferError:
        print('метод переполнения буфера проходили. гуляй')
        return redirect(url_for('edit_post', post_id=int(the_post.id), project=int(project)))
    except RuntimeError:
        print('по моему кто-то пытается нас хакнуть ss')
        return redirect(url_for('edit_post', post_id=int(the_post.id), project=int(project)))

@app.route('/edit_post/<post_id>', methods=['GET', 'POST']) #что такое methods
@login_required
#@spec_required #дописать
def edit_post(post_id,project=None):
    project = request.args.get('project', None)
    post={}
    if (post_id != 'new_post'):
        post_obj = Post.query.filter_by(id=int(post_id)).first_or_404()
        post = {
            'BODY'           : post_obj.body,
            'SOCIAL_NETWORK' : post_obj.sosial_network,
            'STATUS'         : post_obj.status,
            'TIME'           : str(post_obj.time),
            'TOPIC'          : post_obj.topic }
    form = EditPostForm()

    toDraft = request.form.get('toDraft')
    submit = request.form.get('submit')
    reLook = request.form.get('reLook')
    if submit:
        if (post_id == 'new_post'):
            #print('\n\n\n\n\nXXXXXXXXXXXXX1', id)
            add_post_to_db(topic=form.topic.data, body=form.body.data, network=form.network.data, time=form.time.data, project=project, status=1)
        else:
            filenames_dict = upload_file(post_id, project)
            #print('\n\n\n\n\nXXXXXXXXXXXXX2', id)
            add_post_to_db(topic=form.topic.data, body=form.body.data, network=form.network.data, time=form.time.data, project=project, media=filenames_dict, status=post_obj.status, id=post_obj.id)
        flash('Vash post dobavlen')
        return redirect(url_for('spec_projects', project=int(project), filter=1, quantity=5))

    if toDraft: #and (post_id == 'new_post'):
        #the_post_id=add_post_to_db(topic=form.topic.data, body=form.body.data, network=form.network.data, time=form.time.data, project=project, status=6)
        if (post_id == 'new_post'):
            the_post_id=add_post_to_db(topic=form.topic.data, body=form.body.data, network=form.network.data, time=form.time.data, project=project, status=1)
        else:
            filenames_dict = upload_file(post_id, project)
            the_post_id=add_post_to_db(topic=form.topic.data, body=form.body.data, network=form.network.data, time=form.time.data, media=filenames_dict, project=project, status=post_obj.status, id=post_obj.id)
        flash('Vash post sohranen')
        return redirect(url_for('edit_post', post_id=the_post_id, project=int(project)))
    if reLook:
        post = {
            'BODY'           : form.body.data,
            'SOCIAL_NETWORK' : form.network.data,
            'STATUS'         : 6,
            'TIME'           : str(form.time.data),
            'TOPIC'          : form.topic.data }

        return render_template('post_preview.html', post=post, project=project)
    # if post_id==None:
    #     print('создаём новый пост')
    #     the_post=Post(sosial_network=network, topic=topic, body=body, status=status, user_id=current_user.id, project_id=current_project, time=time)
    #     try:
    #
    #         the_post=Post.query.filter_by(id=int(post_id)).first()
    #         the_post.status = int(set_status)
    #         db.session.add(the_post)
    #         db.session.commit()
    #     except ValueError:
    #         print('не тот тип данных прилетел в json')
    #     except BufferError:
    #         print('метод переполнения буфера проходили. гуляй')
    #     except RuntimeError:
    #         print('по моему кто-то пытается нас хакнуть')


    #WORKING PART but
    # if toDraft:
    #     print('to Draft')
    ## elif request.method == 'GET':
    # ####form.username.data = current_user.username
    #---------------------------
    #WORKING PART, BUT searching
    # if request.method == "POST":
    #     tmp=request.form['toDraft']
    #     if tmp:
    #         print('tmp')
    # ----------------------------------- #

    # post_object = Post.query.filter_by(id=post_id).first_or_404()
    # post_dict = {
    #     'body'       : post_object.body,
    #     'time'       : post_object.time,
    #     'network'    : post_object.sosial_network,
    #     'topic'      : post_object.topic,
    #     'status'     : post_object.status
    # }
    # #TODO: проверить на
    # form = EditPostForm()
    # form.body.data = post_dict['body']
    # form.network.data = post_dict['network']
    # form.topic.data = post_dict['topic']
    # form.time.data = post_dict['time']
    # print('xxxxxx')
    # if form.validate_on_submit():
    #     post_object.body = form.body.data
    #     #post_object.status = form.status.data
    #     post_object.sosial_network = form.network.data
    #     post_object.topic = form.topic.data
    #     post_object.time = form.time.data
    #     db.session.add(post_object)
    #     db.session.commit()
    #     flash('Ваши изменения будут сохранены!')
    #     return redirect(url_for('/project'))#дописать, чтоб возвращало на тот же проект

    return render_template('post_edit.html', form=EditPostForm(), post=post)#, post=post_dict

@app.route('/spec_projects/<project>', methods=['GET'])
@login_required #spec_required
#@requires_spec
@owner_required
def spec_projects(project,filter=None,quantity=None): #копипаст projects с небольшими правками
    print("\n\n\n\n\n", project, "\n\n\n\n\n\n")

    print("\n\n\n\n\n", project, "\n\n\n\n\n\n")
    filter = request.args.get('filter', None)
    if (filter == None):
        filter = 1
    quantity = request.args.get('quantity', None) #количество
    print('фильтр такой', filter, 'а их количество:', quantity)
    try:
        if filter != None:
            filter=int(filter)
        if quantity != None:
            quantity=int(quantity)
    except ValueError:
        print('не верный формат get запроса')
    except BufferError:
        print('переполнение буфера')
    except RuntimeError:
        print('по моему кто-то пытается нас хакнуть')

    Projects_of_current_user_list=[]
    User_projects_list = Users_Projects.query.filter_by(user_id=current_user.id, asses=1).all()

    #print(User_projects_list)

    for iter_project in User_projects_list:
        tmp = Project.query.filter_by(id=iter_project.project_id).first()
        Projects_of_current_user_list.append({'name' : tmp.name, 'id' : tmp.id})
    print(len(User_projects_list))
    if len(User_projects_list)>0 and project=='first':
        project = User_projects_list[0].project_id

    all_posts = []
    if (len(User_projects_list) != 0) and project=='first':
        project = User_projects_list[0].project_id
    if len(User_projects_list)==0:
        print('This user hasn\'t got projects!')
        project = -1
    elif filter!=None:
        if (project != 'first'):
            all_posts = Post.query.filter_by(project_id=int(project), status=filter).all()
    else:
        if (project != 'first'):
            all_posts = Post.query.filter_by(project_id=int(project)).all()

    posts_list = get_list_of_post_dicts(all_posts)
    print(all_posts)


    if quantity!=None:
        posts_list=posts_list[0:quantity]

    print('\n\n\n')
    print(Projects_of_current_user_list)
    print()
    print(project)
    print('\n\n\n')

    return render_template('project_spec.html', filter=str(filter), user=current_user, Posts=posts_list, Projects=Projects_of_current_user_list, current_project=int(project))

#------hm_hm_1
@app.route('/create_post', methods=['POST', 'GET'])
def create_post():
    args = {'method': 'GET'}
    if request.method == 'POST':
        file = request.files['file']
        if bool(file.filename):
            file_bytes = file.read(MAX_FILE_SIZE)
            args['file_size_error'] = len(file_bytes) == MAX_FILE_SIZE
        args['method'] = 'POST'
    return render_template('create_post.html', args=args)

if __name__ == '__main__':
    app.run(debug=True)
#------hm_hm_2
@app.route('/jsontmp', methods=['POST', 'GET'])#only tmp
def jsontmp():
    our_format={'ui': 1, 'pr': 2, 'pi':3, 'i':'123456789.png', 'v':'123456789.mp4'}
    return json.dumps(our_format)
