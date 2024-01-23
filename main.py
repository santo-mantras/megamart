from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from application.models import db, User, Role
from application.resources import api
from config import DevelopmentConfig 
from application.sec import datastore
from application.resources import api
from application.worker import celery_init_app
from application.tasks import *
import flask_excel as excel
from celery.schedules import crontab
from application.cache_instance import cache 




def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app) # Application knows it is using flask sqlaclhemy instance
    api.init_app(app)
    excel.init_excel(app)
    datastore = SQLAlchemyUserDatastore(db,User,Role)
    app.security = Security(app,datastore)
    cache.init_app(app)
    with app.app_context():
        import application.views
        #cache.clear()

    return app,datastore

app, datastore = create_app()
celery_app = celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(30.0,
        daily_reminder.s(daily_reminder("sam@abc.coming","Monthly-report"),"ok"),
    )


if __name__ == "__main__":
    app.run(debug=True)


    
#crontab(hour=13, minute=46),    
    
    
    
    