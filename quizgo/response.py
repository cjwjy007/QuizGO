from flask import jsonify


class Response:
    def __init__(self):
        pass

    def ok(self, msg=None, data=None):
        if msg is None:
            msg = "success"
        if data is None:
            return jsonify({
                'stateCode': 200,
                'msg': msg,
            })
        else:
            return jsonify({
                'stateCode': 200,
                'msg': msg,
                'data': data
            })

    def err(self, msg=None, data=None):
        if msg is None:
            msg = "error"
        if data is None:
            return jsonify({
                'stateCode': 404,
                'msg': msg,
            })
        else:
            return jsonify({
                'stateCode': 404,
                'msg': msg,
                'data': data
            })
