from app import db
from app.models import User, Meals, Nutrision

def save_predictions(user_id, predictions):
    user = User.query.get(user_id)
    if not user:
        # Buat entri baru untuk pengguna jika belum ada
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return "User not found"
    
    for prediction in predictions:
        label = prediction['label']
        confidence = prediction['confidence']
        
        # Cari nutrisi berdasarkan label    
        nutrition = Nutrision.query.filter_by(name=label).first()
        if not nutrition:
            # Jika label tidak ditemukan dalam tabel Nutrision, Anda dapat melakukan penanganan khusus di sini
            # Misalnya, mengisi nilai nutrisi dengan nilai default atau memberikan pesan kesalahan
            return f"Nutrition information for {label} not found"
        
        # Simpan prediksi ke dalam tabel Meals
        meals = Meals(
            meals_name=label,
            calories=nutrition.calories,
            carbs=nutrition.carbs,
            proteins=nutrition.proteins,
            fats=nutrition.fats,
            minerals=nutrition.minerals,
            user=user
        )
        db.session.add(meals)
    
    db.session.commit()
    return "Predictions saved successfully"
