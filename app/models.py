from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Meals(db.Model):
    mealId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meals_name = db.Column(db.String(255))
    calories = db.Column(db.Float)
    carbs = db.Column(db.Float)
    proteins = db.Column(db.Float)
    fats = db.Column(db.Float)
    minerals = db.Column(db.Float)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('meals', lazy=True))

    def __repr__(self):
        return f'<Meals {self.meals_name}>'
    
class Nutrision(db.Model):
    nutrisionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    proteins = db.Column(db.Float, nullable=False)
    fats = db.Column(db.Float, nullable=False)
    minerals = db.Column(db.Float, nullable=False)