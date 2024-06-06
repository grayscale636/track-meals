from app import app, db
from app.models import Nutrision

foodNutritionMap = {
    "Alpukat": {"calories": 85, "proteins": 0.9, "fats": 6.5, "carbs": 7.7, "minerals": 84.3},
    "Dada Ayam": {"calories": 150, "proteins": 28.74, "fats": 3.0, "carbs": 0.0, "minerals": 0.0},
    "Jeruk": {"calories": 45, "proteins": 0.9, "fats": 0.2, "carbs": 11.2, "minerals": 87.2},
    "Tumis Kangkung": {"calories": 39, "proteins": 2.6, "fats": 2.7, "carbs": 3.1, "minerals": 0.0},
    "Nasi Merah": {"calories": 149, "proteins": 2.8, "fats": 0.4, "carbs": 32.5, "minerals": 64.0},
    "Nasi Putih": {"calories": 180, "proteins": 3.0, "fats": 0.3, "carbs": 39.8, "minerals": 56.7},
    "Salmon": {"calories": 179, "proteins": 19.93, "fats": 10.43, "carbs": 0.0, "minerals": 71.64},
    "Sayur Bayam": {"calories": 16, "proteins": 0.9, "fats": 0.4, "carbs": 2.9, "minerals": 94.5},
    "Telur Goreng": {"calories": 196, "proteins": 14.0, "fats": 15.0, "carbs": 0.9, "minerals": 0.0},
    "Telur Rebus": {"calories": 155, "proteins": 13.0, "fats": 11.0, "carbs": 1.1, "minerals": 0.0},
    "Tempe Goreng": {"calories": 336, "proteins": 20.0, "fats": 28.0, "carbs": 7.8, "minerals": 42.9}
}

with app.app_context():
    nutrision_id = 1
    for food, nutrition_data in foodNutritionMap.items():
        nutrision = Nutrision(
            nutrisionId=nutrision_id,
            name=food,
            calories=nutrition_data["calories"],
            carbs=nutrition_data["carbs"],
            proteins=nutrition_data["proteins"],
            fats=nutrition_data["fats"],
            minerals=nutrition_data["minerals"]
        )
        db.session.add(nutrision)
        nutrision_id += 1
    db.session.commit()