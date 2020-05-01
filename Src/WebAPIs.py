from pathlib import Path

import numpy as np
from flask import request
from keras.models import model_from_json
from keras.preprocessing import image

from Src.models import *
from Util.database import db, dbmodel_to_jsonlist
from Util.response import json_response
from appConfig import app


# region admin

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


# endregion

@app.route('/api/ClassifyMammogram')
def ClassifyMammogram():
    # args
    mammogram_path = request.args['path']

    model_json_path = Path('CNN/model.json')
    model_h5_path = Path('CNN/model.h5')
    json_file = open(model_json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into a model
    model.load_weights(model_h5_path)

    mammogram = image.load_img(mammogram_path, target_size=(64, 64))
    mammogram = image.img_to_array(mammogram)
    mammogram = np.expand_dims(mammogram, axis=0)
    result = model.predict(mammogram)

    if result[0][0] == 0:
        prediction = 'abnormal'
    else:
        prediction = 'normal'

    return json_response(prediction)
