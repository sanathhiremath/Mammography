from flask import jsonify


def json_response(result={}, error="none"):
    return jsonify({"result": result, "error": error})
