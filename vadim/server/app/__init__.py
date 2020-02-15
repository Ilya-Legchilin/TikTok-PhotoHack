from flask import Flask, redirect, url_for, request, Response
from werkzeug.exceptions import HTTPException
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import flask_admin as admin #добавляем админа
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import BooleanEqualFilter


app = Flask(__name__)
UPLOAD_FOLDER = 'static'
#app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 99 * 1024 * 1024
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models

app.config['ADMIN_CREDENTIALS'] = ('admin', 'qwerty')

class FlaskyAdminIndexView(admin.AdminIndexView):
    @admin.expose('/')
    def index(self):
        print('ping 8.8.8.8')
        # if current_user.is_authenticated:     ###FICHA
        #     print('ping')                     ###FICHA
        # else:                                 ###FICHA
        #     return redirect(url_for('index')) ###FICHA
        return super(FlaskyAdminIndexView, self).index()

    def is_accessible(self):
        auth = request.authorization or request.environ.get('REMOTE_USER')  # workaround for Apache
        if not auth or (auth.username, auth.password) != app.config['ADMIN_CREDENTIALS']:
            raise HTTPException('', Response(
                "Please log in.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))
        return True

admin = admin.Admin(index_view=FlaskyAdminIndexView(),name="диспетер СММ", template_mode='bootstrap3')

class UserView(ModelView):
    can_delete = True#False  # disable model deletion
    can_create = True#False
    can_edit = True
    #excluded_list_columns = ('password_hash',)
    #column_filters = (BooleanEqualFilter(column=routes.User.week, name='Week'),)

class PostView(ModelView):
    page_size = 50  # the number of entries to display on the list view

admin.add_view(UserView(routes.User, db.session))
admin.add_view(UserView(routes.Post, db.session))
admin.add_view(UserView(routes.Project, db.session))
admin.add_view(UserView(routes.Users_Projects, db.session))

admin.init_app(app)
