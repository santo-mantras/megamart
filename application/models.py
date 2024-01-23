from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class User(db.Model, UserMixin):
  #__tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String, unique=False)
  email = db.Column(db.String, unique=True)
  password = db.Column(db.String(255))
  active = db.Column(db.Boolean())
  fs_uniquifier = db.Column(db.String(255),unique=True, nullable = False)
  roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
  #role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
  #role = db.relationship('Role')
  category = db.relationship('Category', backref = 'creator')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Category(db.Model):
  #__tablename__ = 'Category'
   id = db.Column(db.Integer, primary_key=True)
   category_name = db.Column(db.String, unique=True, nullable=False)
   category_descr = db.Column(db.String, nullable=False)
   creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
   is_approved = db.Column(db.Boolean(), default=False)
   to_delete = db.Column(db.Boolean(), default=False)

class Category_Temp(db.Model):
  #__tablename__ = 'Category_Temp'
   #id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True, autoincrement = True, nullable = False)
   id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable = False)
   cat_id = db.Column(db.Integer, db.ForeignKey('category.id'),  nullable = False)
   category_name = db.Column(db.String, unique=True, nullable=False)
   category_descr = db.Column(db.String, nullable=False)
   creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
   is_approved = db.Column(db.Boolean(), default=False)
   
   
"""
class Products(db.Model):
  #__tablename__ = 'Product'
  Product_Id = db.Column(db.Integer, primary_key=True)
  Product_Name = db.Column(db.String, unique=True, nullable=False)
  Product_Unit = db.Column(db.String, nullable=False)
  Product_Price = db.Column(db.Integer, nullable=False)
  Product_Quantity = db.Column(db.Integer, nullable=False)
  Product_ExpiryDate = db.Column(db.String)
"""