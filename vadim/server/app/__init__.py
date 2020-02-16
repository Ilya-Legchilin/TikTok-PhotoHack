import os
# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
import json
from functools import wraps
import os
import urllib.request
from werkzeug.utils import secure_filename
from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/main')
def index():
    return render_template("main_page.html")

@app.route('/upl_vid')
def upl_vid():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
        files = request.files.getlist('files[]')
        for file in files:
            if file:# and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                #type = get_type(filename)
                directory = os.path.join("video")
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file.save(os.path.join(directory, filename))

        flash('File(s) successfully uploaded')
    return render_template("upload_video.html")

@app.route('/upl_ph')
def upl_ph():
    return render_template("upload_photo.html")

@app.route('/photo_uploader', methods = ["GET", "POST"])
def photo_uploader():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            directory = os.path.join("photo")
            if not os.path.exists(directory):
                os.makedirs(directory)
            file.save(os.path.join(directory, filename))
        return redirect(url_for("upl_ph"))

@app.route('/video_uploader', methods = ["GET", "POST"])
def video_uploader():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            flash('No file part')
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            directory = os.path.join("video")
            if not os.path.exists(directory):
                os.makedirs(directory)
            file.save(os.path.join(directory, filename))
        return redirect(url_for("upl_vid"))

app.run()
