from main import app
from application.sec import datastore
from application.models import db, Role
from werkzeug.security import generate_password_hash 
#from __future__ import absolute_import
#from .celery import app as celery_app
from application.worker import celery_init_app   

with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="Admin User")
    datastore.find_or_create_role(name="storemanager", description="Store Manager User")
    datastore.find_or_create_role(name="customer", description="Customer User")
    db.session.commit()
    if not datastore.find_user(email="admin@email.com"):
        datastore.create_user(email="admin@email.com", password=generate_password_hash("admin1234"), roles=["admin"])

    if not datastore.find_user(email="storemanager1@email.com"):
        datastore.create_user(email="storemanager1@email.com", password=generate_password_hash("abc1234"), roles=["storemanager"], active=False)
    
    if not datastore.find_user(email="customer1@email.com"):
        datastore.create_user(email="customer1@email.com", password=generate_password_hash("shop1234"), roles=["customer"])

    db.session.commit()
    """
    admin = Role(id='admin', name='Admin',description='Admin User')
    db.session.add(admin)
    store_manager = Role(id='store_manager', name='StoreManager',description='Store Manager User')
    db.session.add(store_manager)
    customer = Role(id='customer', name='Cusotmer',description='Cusotmer User')
    db.session.add(customer)
    try:
        db.session.commit()
    except:
        pass
    """