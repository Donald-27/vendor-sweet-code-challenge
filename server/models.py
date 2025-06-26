from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendor_sweets = db.relationship('VendorSweet', backref='sweet', cascade='all, delete-orphan')

    # Add serialization
   
    serialize_rules = ('-vendor_sweets.sweet',)

    def __repr__(self):
        return f'<Sweet {self.id}>'


class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationship
    vendor_sweets = db.relationship('VendorSweet', backref='vendor', cascade='all, delete-orphan')

    # Add serialization
    serialize_rules = ('-vendor_sweets.vendor',)

    def __repr__(self):
        return f'<Vendor {self.id}>'


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'))

    # Add relationships
  

    # Add serialization
    serialize_rules = (
        'vendor', 'sweet',
        '-vendor.vendor_sweets', '-sweet.vendor_sweets',
    )

    # Add validation
    @validates('price')
    def validate_price(self, key, value):
        if type(value) is not int or value is None or value < 0:
            raise ValueError('Price must be a non-negative integer.')
        return value

    def __repr__(self):
        return f'<VendorSweet {self.id}>'
