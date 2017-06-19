from app import db
from flask import Blueprint, jsonify
from app.models import Category, Item

api = Blueprint('api', __name__)


@api.route('/catalog.json')
def restaurantsJSON():
    categories = db.session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])
