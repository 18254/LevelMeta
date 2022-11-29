from unicodedata import category
from shop import db
from datetime import datetime
from sqlalchemy.orm import relationship, backref

categorys = db.Table('categorys',
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
    db.Column('addproduct_id', db.Integer, db.ForeignKey('addproduct.id'), primary_key=True)
)#many to many relationship joining table 

class Addproduct(db.Model):
    __seachbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False, default='image1.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image2.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image3.jpg')

    categorys = db.relationship('Category', secondary=categorys, lazy='subquery',
        backref=db.backref('addproduct', lazy=True))
        #many to many joining table 

    def __repr__(self):
        return '<Post %r>' % self.name
        #admin entries images and other inforation added to the database 



class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    #brands to choose from to add to products 

    def __repr__(self):
        return '<Brand %r>' % self.name

    
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
#categories to choose from to add to products 
    def __repr__(self):
        return '<Catgory %r>' % self.name





db.create_all()
#adds table to the database