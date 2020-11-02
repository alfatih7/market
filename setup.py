import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "marketdb"
database_path = "postgres://{}:{}@{}/{}".format(
    'postgres', '1993239', 'localhost:5432', database_name)

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()


'''''''''''''''''''''''''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''''''''''''''''

'''
Category

'''


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    item = db.relationship('Item', backref='item', lazy=True)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type,
            'item': self.item
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Item(db.Model):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    origin_price = Column(String, nullable=False)
    sale_pric = Column(String, nullable=False)
    count = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id))

    def __init__(self, name, origin_price, sale_pric, count, category_id):
        # self.id = id
        self.name = name
        self.origin_price = origin_price
        self.sale_pric = sale_pric
        self.count = count
        self.category_id = category_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'origin_price': self.origin_price,
            'sale_price': self.sale_pric,
            'count': self.count,
            # 'category_id': self.category_id
        }

    def search_qustion(self, search, q_s):
        if search in q_s:
            return {
                "title: ": self.question

            }
