from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    serialize_rules = ('-reviews.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy: lets you access items directly
    items = association_proxy('reviews', 'item')

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    serialize_rules = ('-reviews.item',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='item')

    # Association proxy: lets you access customers directly
    customers = association_proxy('reviews', 'customer')

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ('-customer.reviews', '-item.reviews')

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # Relationships back to Customer and Item
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    comment = db.Column(db.String)

    def __repr__(self):
        return f'<Review {self.id}, rating={self.rating}>'