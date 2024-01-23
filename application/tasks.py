import flask_excel as excel
import csv
import os
from celery import shared_task
from .models import Category, User, Role
from .mail_service import send_message

@shared_task(ignore_result=False)
def create_resource_csv():

    cat_res = Category.query.with_entities(Category.category_name, Category.category_descr).all()
    csv_output = excel.make_response_from_query_sets(cat_res, ["category_name", "category_descr"], "csv")
    filename="sample.csv"

    with open(filename, 'wb')  as f:
        f.write(csv_output.data)
    return filename


    
#@shared_task(ignore_result=True)
@shared_task(ignore_result=True)
def daily_reminder(to, subject):
    users = User.query.filter(User.roles.any(Role.name=='customer')).all()
    #send_message('sam@email.com','Test', '<html> One </html>')
    #send_message(to, subject, "Hello")
    #send_message("Sam@Daily.com", "Daily", "Hello")
    for user in users:
        send_message(user.email, subject, "HI User")
    return send_message(user.email, subject, "HI User")

#send_message("Sam@Daily.com", "Daily", "Hello")