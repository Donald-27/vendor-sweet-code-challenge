from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Sweet, Vendor, VendorSweet
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

@app.route('/')
def index():
    return '<h1>VendorSweets Code Challenge</h1>'

# -------------------------------
#           API ROUTES
# -------------------------------

class Vendors(Resource):
    def get(self):
        vendors = Vendor.query.all()
        return [{'id': v.id, 'name': v.name} for v in vendors], 200

api.add_resource(Vendors, '/vendors')

class VendorByID(Resource):
    def get(self, id):
        vendor = Vendor.query.get(id)
        if vendor:
            return make_response(vendor.to_dict(), 200)
        return make_response({'error': 'Vendor not found'}, 404)

api.add_resource(VendorByID, '/vendors/<int:id>')

class Sweets(Resource):
    def get(self):
        sweets = Sweet.query.all()
        return [{'id': s.id, 'name': s.name} for s in sweets], 200

api.add_resource(Sweets, '/sweets')

class SweetByID(Resource):
    def get(self, id):
        sweet = Sweet.query.get(id)
        if sweet:
            return make_response({
                'id': sweet.id,
                'name': sweet.name
                # test expects no vendor_sweets in this response
            }, 200)
        return make_response({'error': 'Sweet not found'}, 404)

api.add_resource(SweetByID, '/sweets/<int:id>')

class VendorSweets(Resource):
    def post(self):
        data = request.get_json()
        try:
            price = data['price']
            vendor_id = data['vendor_id']
            sweet_id = data['sweet_id']
            new_vs = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
            db.session.add(new_vs)
            db.session.commit()
            return make_response(new_vs.to_dict(), 201)
        except Exception:
            return make_response({"errors": ["validation errors"]}, 400)

api.add_resource(VendorSweets, '/vendor_sweets')

class VendorSweetByID(Resource):
    def delete(self, id):
        vs = VendorSweet.query.get(id)
        if vs:
            db.session.delete(vs)
            db.session.commit()
            return '', 204
        return make_response({"error": "VendorSweet not found"}, 404)

api.add_resource(VendorSweetByID, '/vendor_sweets/<int:id>')
