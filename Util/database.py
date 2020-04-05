from appConfig import app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
Migrate(app, db)


# Convert db model to json object
def dbmodel_to_jsonlist(model_data):
    data_list = []
    for row in model_data:
        data = {}
        for key in row.__dict__:
            if key != '_sa_instance_state':
                data[key] = row.__dict__[key]
        data_list.append(data)
    return data_list
