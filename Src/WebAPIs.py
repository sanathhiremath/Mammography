from flask import request
from Src.models import *
from Util.database import db, dbmodel_to_jsonlist
from Util.response import json_response
from appConfig import app


@app.route('/api/IsUserExists')
def is_user_exists():
    # args
    email = request.args['email']
    user_type = request.args['user_type']

    is_exists = False
    user = db.session.query(user_type_dict[user_type]).filter_by(email=email)
    if user.count() > 0:
        is_exists = True
    return json_response(is_exists)


@app.route('/api/GetUserDetails')
def get_user_details():
    # args
    email = request.args['email']
    user_password = request.args['user_password']
    user_type = request.args['user_type']

    user = db.session.query(user_type_dict[user_type]).filter_by(email=email, password=user_password)
    res = dbmodel_to_jsonlist(user)
    return json_response(res)
