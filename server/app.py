#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    # Simple index route to confirm the app is running
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


@app.route("/earthquakes/<int:id>")
def get_earthquake(id):
    """
    View to get a single Earthquake by its id.
    Returns JSON with earthquake details if found,
    otherwise returns a 404 with an error message.
    """
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return jsonify(
            {
                "id": earthquake.id,
                "location": earthquake.location,
                "magnitude": earthquake.magnitude,
                "year": earthquake.year,
            }
        ), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude):
    """
    View to get all earthquakes with magnitude greater than or equal
    to the provided magnitude value.
    Returns JSON with a count and list of matching earthquakes.
    """
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quakes_list = [
        {"id": q.id, "location": q.location, "magnitude": q.magnitude, "year": q.year}
        for q in quakes
    ]

    return jsonify({"count": len(quakes_list), "quakes": quakes_list}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
