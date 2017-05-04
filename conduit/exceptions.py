from flask import jsonify


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = dict(self.payload or ())
        rv = self.message
        return jsonify(rv)


def TEMPLATE(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


USER_NOT_FOUND = TEMPLATE(['User not found'], code=404)
USER_ALREADY_REGISTERED = TEMPLATE(['User already registered'], code=422)
