from flask import current_app as app, jsonify, request, render_template, send_file
from flask_security import auth_required, roles_required, roles_accepted
from werkzeug.security import check_password_hash
from flask_restful import marshal, fields
import flask_excel as excel
from celery.result import AsyncResult
from .models import User, db, Category, Category_Temp
from .sec import datastore
from .tasks import create_resource_csv


@app.get('/')
def home():
    return render_template("index.html")

@app.get('/admin')
@auth_required("token")
@roles_required("admin")
def admin():
    return "Hello Admin !!"

@app.get('/activate/storemanager/<int:strmngr_id>')
@auth_required("token")
@roles_required("admin")
def activate_storemanager(strmngr_id):
    store_manager = User.query.get(strmngr_id)
    if not store_manager or "storemanager" not in store_manager.roles:
        return jsonify({"message":"Store Manager not found"}), 404
    
    store_manager.active = True
    db.session.commit()
    return jsonify({"message":"Store Manager Activated"})

@app.post('/user-login')
def user_login():
    data = request.get_json()
    email = data.get('email')
    if not email:
         return jsonify({"message":"Email not provided"}), 400
    
    user = datastore.find_user(email=email)

    if not user:
        return jsonify({"message":"User not found"}), 404

    if check_password_hash(user.password, data.get("password")):
        return jsonify({"token":user.get_auth_token(), "email":user.email, "role":user.roles[0].name})
        #return user.get_auth_token()
    else:
        return jsonify({"message":"Incorrect Password"}), 400

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "active": fields.Boolean
}

class Creator(fields.Raw):
    def format(self, user):
        return user.email

category_fields = {
    'id': fields.Integer,
    'category_name':   fields.String,
    'category_descr':   fields.String,
    'is_approved': fields.Boolean,
    'creator_id': fields.Integer,
    'creator': Creator
}

@app.get('/users')
@auth_required("token")
@roles_required("admin")
def all_users():
    users = User.query.all()
    if len(users) == 0:
        return jsonify({"message": "No User Found"}), 404
    return marshal(users, user_fields)

@app.get('/editrequest')
@auth_required("token")
@roles_required("admin")
def all_request():
    editrequest = Category_Temp.query.all()
    if len(editrequest) == 0:
        return jsonify({"message": "No request Found"}), 404
    return marshal(editrequest, category_fields)

@app.get('/category-resource/<int:id>/approve')
@auth_required("token")
@roles_required("admin")
def resource(id):
    cat = Category.query.get(id)
    if not cat:
        return jsonify({"message": "Resource Not found"}), 404
    cat.is_approved = True
    db.session.commit()
    return jsonify({"message": "Category Approved"})

@app.get('/category-resource/<int:id>/category_delete')
@auth_required("token")
@roles_required("storemanager")
def cat_resource(id):
    cat = Category.query.get(id)
    if not cat:
        return jsonify({"message": "Resource Not found"}), 404
    cat.to_delete = True
    db.session.commit()
    return jsonify({"message": "Request Sent for Approval to Admin"})

@app.get('/category-resource/<int:id>/category_delete_admin')
@auth_required("token")
@roles_required("admin")
def cat_del(id):
    cat = Category.query.get(id)
    if not cat:
        return jsonify({"message": "Resource Not found"}), 404
    #Category.query.get(id).delete()
    db.session.delete(cat)
    db.session.commit()
    return jsonify({"message": "Category Deleted"})
"""
@app.get('/category-resource/<int:id>/editedCategory')
@auth_required("token")
@roles_accepted('admin', 'storemanager')
def cat_update(id):
    cat = Category.query.get(id)
    form = request.get_json()
    #cat_id=form['id']
    cat_name = form.get('category_name')
    cat_desc = form.get('category_descr')
    print(cat_name,cat_desc)
    if not cat:
        return jsonify({"message": "Resource Not found"}), 404
    cat.category_name=cat_name
    cat.category_descr=cat_desc
    cat.is_approved = False
    #db.session.add(cat)
    return jsonify({"message": "Request Sent for Approval to Admin"})
"""
@app.get('/category-resource/<int:cat_id>/approve-edit')
@auth_required("token")
@roles_required("admin")
def approve_edit(cat_id):
    cat = Category_Temp.query.get(id)
    if not cat:
        return jsonify({"message": "Resource Not found"}), 404
    cat.is_approved = True
    db.session.commit()
    return jsonify({"message": "Category Approved"})

@app.get('/category-resource/<int:cat_id>/reject-edit')
@auth_required("token")
@roles_required("admin")
def reject_edit(cat_id):
    cat = Category_Temp.query.get(id)
    if not cat:
        return jsonify({"message": "Resource Not found"}), 404
    db.session.delete(cat)
    db.session.commit()
    return jsonify({"message": "Edit Request Rejected"})

@app.get('/download-csv')
def download_csv():
    #cat_res = Category.query.with_entities(Category.category_name, Category.category_descr).all()
    #csv_output = excel.make_response_from_query_sets(cat_res, ["category_name", "category_descr"], "csv", filename="test1.csv")
    #return csv_output
    task0 = create_resource_csv()
    task = create_resource_csv.delay()
    return jsonify({"task-id" : task.id})

@app.get('/get-csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    #print(res)
    if res:
        filename = res.result
        return send_file(path_or_file='sample.csv', as_attachment=True)
        #return jsonify({"message" : "task complete"})
    else:
        return jsonify({"message" : "task pending"}), 404

"""
@app.get('/study-resource/<int:id>/approve')
@auth_required("token")
@roles_required("storemanager")
def resource(id):
    cat = Category.query.get(id)
    if not cat:
        return jsonify({"message": "Resource Not found"}), 404
    cat.is_approved = True
    db.session.commit()
    return jsonify({"message": "Aproved"})
"""