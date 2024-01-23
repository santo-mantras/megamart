from flask_restful import Resource, Api, reqparse, fields, marshal
from flask_security import auth_required, roles_required, current_user, roles_accepted
from flask import jsonify, request
from sqlalchemy import or_
from .models import Category, db, User, Role, RolesUsers, Category_Temp
from werkzeug.security import generate_password_hash 
from application.sec import datastore
from .cache_instance import cache


api = Api(prefix='/api')

parser = reqparse.RequestParser()
parser.add_argument('category_name', type=str, help='Category Name is required should be a string', required=True)
parser.add_argument('category_descr', type=str, help='Category description is required and should be a string', required=True)

class Creator(fields.Raw):
    def format(self, user):
        return user.email

category_fields = {
    'id': fields.Integer,
    'category_name':   fields.String,
    'category_descr':   fields.String,
    'is_approved': fields.Boolean,
    'to_delete': fields.Boolean,
    'creator': Creator
}

class CategorySection(Resource):
    #@auth_required("token")
    #@cache.cached(timeout=50)
    def get(self):
        if "admin" in current_user.roles:
            all_categ_fields = Category.query.all()
        else:
            all_categ_fields = Category.query.filter(or_(Category.is_approved == True, Category.creator == current_user)).all()
        if len(all_categ_fields) > 0 :
            return marshal(all_categ_fields, category_fields)
        else:
            return {"message":"Not Found"}, 404
    @auth_required("token")
    @roles_accepted('admin', 'storemanager')
    #@roles_required("storemanager")
    def post(self):
        args = parser.parse_args()
        categ = Category(category_name=args.get("category_name"), category_descr=args.get("category_descr"), creator_id=current_user.id)
        db.session.add(categ)
        db.session.commit()
        return {"message":"Category Created"}
api.add_resource(CategorySection, '/category_section')

class CategoryUpdate(Resource):
    @auth_required("token")
    @roles_accepted('admin', 'storemanager')
    def post(self):
        form = request.get_json()
        args = parser.parse_args()
        cat_name = form.get('category_name')
        cat_desc = form.get('category_descr')
        cat_id = form.get('id')
        print(cat_id,cat_name,cat_desc,cat_id)
        if not cat_name:
            return {"message":"Category Name not provided"}, 400
        if "admin" in current_user.roles:
            categ1 = Category.query.filter_by(id=cat_id).first()
            categ1.category_name = form.get('category_name') 
            categ1.category_descr = form.get('category_descr')
            categ1.creator_id = current_user.id
            db.session.add(categ1)
            db.session.commit()
            return {"message":"Category Updated by Admin"}
        if "storemanager" in current_user.roles:
            cat_name = form.get('category_name')
            cat_desc = form.get('category_descr')
            #categ1 = Category_Temp(id=cat_id, category_name=cat_name, category_descr=cat_desc, creator_id=current_user.id)
            categ1 = Category_Temp(cat_id=cat_id, category_name=args.get("category_name"), category_descr=args.get("category_descr"), creator_id=current_user.id)
            db.session.add(categ1)
            db.session.commit()
            return {"message":"Update Request Sent to Admin for Approval"}
        else:
            return {"message":"Failed to Update"}
        #print(cat_name, cat_desc)
        #categ = Category(category_name=cat_name, category_descr=cat_desc, creator_id=current_user.id)
        #categ1 = Category(category_name=args.get("category_name"), category_descr=args.get("category_descr"), creator_id=current_user.id)
        #db.session.add(categ1)
        #db.session.commit()
#api.add_resource(CategoryUpdate, '/<int:id>/editCategory')
api.add_resource(CategoryUpdate, '/editCategory')



parser2 = reqparse.RequestParser()
parser2.add_argument('email', type=str, help='email is required should be a string', required=True)
parser2.add_argument('password', type=str, help='password is required', required=True)
parser2.add_argument('username', type=str, help='username is recommended')
#parser2.add_argument('name', type=str, help='roles is required', required=True)

#class User_Role(fields.Raw):
#    def format(self, user):
#        return user.roles
"""
signup_fields = {
    'id' : fields.Integer,
    'email': fields.String,
    'password': fields.String,
    'username': fields.String, 
    'active':fields.Boolean,
    'fs_uniquifier' : fields.String,
    'roles': fields.List,
}
"""
class Registration(Resource):
    #def get(self):
    #    all_reg_fields = User.query.all()
        #role_name = Role.query.all() 
    #    if len(all_reg_fields) > 0 :
    #        return marshal(all_reg_fields, signup_fields)
    #    else:
    #        return {"message":"Not Found"}, 404
    
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        username = data['username']
        role = data['roles']
        if not email:
            return {"message":"Email not provided"}, 400
        if not password:
            return {"message":"password not provided"}, 400
        if not role:
            return {"message":"Role not provided"}, 400
        #args2 = parser2.parse_args()
        if role == "storemanager" :
            print('role passed as storemanager')
            #reg = User(email=email, password=generate_password_hash(password), username=username, roles=[Role(name="storemanager")],
            #reg = User(email=email, password=generate_password_hash(password), username=username, active=False, )
            datastore.create_user(email=email, password=generate_password_hash(password), username=username, roles=["storemanager"],
            active=False)
            db.session.commit()
        if role == "customer" :
            print('role passed as customer')
            datastore.create_user(email=email, password=generate_password_hash(password), username=username, roles=["customer"])
            db.session.commit()

        return {"message":"User Created"}
api.add_resource(Registration, '/user_signup')
