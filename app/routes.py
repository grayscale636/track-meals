from flask import render_template, flash, redirect, url_for, jsonify, Response, request
from flask_login import current_user, login_user, logout_user, login_required
from functions import load_labels, tflite_detect_objects, generate_frames
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
import numpy as np
import cv2

@app.route('/')
@app.route('/index')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, gender=form.gender.data, age=int(form.age.data))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No image uploaded'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No image uploaded'})

        npimg = np.fromstring(file.read(), np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        labels = load_labels('labelmap.txt')
        detections = tflite_detect_objects(image, labels)
        return jsonify({'predictions': detections})

    return render_template('upload.html')

@app.route('/video_feed')
@login_required
def video_feed():
    labels = load_labels('labelmap.txt')
    return Response(generate_frames(labels), mimetype='multipart/x-mixed-replace; boundary=frame')