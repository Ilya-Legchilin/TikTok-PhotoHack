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

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")
