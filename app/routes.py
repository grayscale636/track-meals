from flask import render_template, flash, redirect, url_for, jsonify, Response, request
from app.models import Meals
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import User, Meals, Nutrision, Prediction
from functions import load_labels, tflite_detect_objects, generate_frames
from app import app, db
from app.forms import LoginForm, RegistrationForm
from .utils import save_predictions
from app.models import User, Prediction, Nutrision
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

@app.route('/profile')
@login_required
def profile():
    user = current_user
    prediction = Prediction.query.all()
    nama_makanan = []
    for food in prediction:
        nama_makanan.append(food.label)
    return render_template('profile.html', user=user, prediction=nama_makanan)

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

@app.route('/save_prediction', methods=['POST'])
def save_predictions_route():
    data = request.json
    prediction_data = data.get('prediction')

    # Ambil pengguna yang saat ini login
    user = current_user

    # Buat objek Prediction baru dan tambahkan ke sesi
    new_prediction = Prediction(
        label=prediction_data['label'],
        confidence=prediction_data['confidence'],
        bbox=str(prediction_data['bbox']),
        user=user
    )
    db.session.add(new_prediction)
    db.session.commit()

    # Lakukan join antara tabel Meals, Nutrision, dan Prediction
    meals_with_predictions = db.session.query(Meals, Nutrision, Prediction)\
        .join(Nutrision, Meals.meals_name == Nutrision.name)\
        .join(Prediction, Meals.meals_name == Prediction.label)\
        .filter(Meals.userId == user.id)\
        .all()

    # Proses hasil join ke dalam format yang sesuai
    formatted_meals_with_predictions = []
    for meal, nutrision, prediction in meals_with_predictions:
        formatted_meals_with_predictions.append({
            'meal_name': meal.meals_name,
            'calories': nutrision.calories,
            'carbs': nutrision.carbs,
            'proteins': nutrision.proteins,
            'fats': nutrision.fats,
            'minerals': nutrision.minerals,
            'prediction_label': prediction.label,
            'prediction_confidence': prediction.confidence,
            'prediction_bbox': prediction.bbox,
            'prediction_time': prediction.prediction_time
        })

    # Lakukan commit ke sesi database
    db.session.commit()

    return jsonify(message='Prediction saved successfully', meals_with_predictions=formatted_meals_with_predictions)




@app.route('/video_feed')
@login_required
def video_feed():
    labels = load_labels('labelmap.txt')
    return Response(generate_frames(labels), mimetype='multipart/x-mixed-replace; boundary=frame')