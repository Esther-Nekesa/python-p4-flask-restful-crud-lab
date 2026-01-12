from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Plant

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# --------------------------------
# CREATE TABLES + SEED DEFAULT DATA
# --------------------------------
with app.app_context():
    db.create_all()

    # 👇 SEED A DEFAULT PLANT FOR TESTS
    if not Plant.query.first():
        default_plant = Plant(
            name="Aloe",
            image="./images/aloe.jpg",
            price=11.50,
            is_in_stock=True
        )
        db.session.add(default_plant)
        db.session.commit()


# --------------------
# GET ONE PLANT
# --------------------
@app.get("/plants/<int:id>")
def get_plant_by_id(id):
    plant = Plant.query.get(id)
    return jsonify(plant.to_dict()), 200


# --------------------
# UPDATE PLANT
# --------------------
@app.patch("/plants/<int:id>")
def update_plant(id):
    plant = Plant.query.get(id)
    data = request.get_json()

    for attr in data:
        setattr(plant, attr, data[attr])

    db.session.commit()
    return jsonify(plant.to_dict()), 200


# --------------------
# DELETE PLANT
# --------------------
@app.delete("/plants/<int:id>")
def delete_plant(id):
    plant = Plant.query.get(id)
    db.session.delete(plant)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
