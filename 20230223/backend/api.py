import common
from dao import DAO
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)
basePath = 'api/v1'
dao = DAO()


def val_body(data):
    if not isinstance(data, str):
        return False
    if not (1 <= len(data) <= 100):
        return False
    return True


def val_topic(topic):
    return isinstance(topic, str)


class PostChirpRes(Resource):
    def post(self):
        data = request.json
        if not val_body(data):
            return None, 400
        id = dao.add_message(data)
        x = dao.get_message(id)
        x['timestamp'] = common.str_from_date(x['timestamp'])
        return x, 201


class GetChirpRes(Resource):
    def get(self, id):
        id = common.uuid_from_str(id)
        if not id:
            return None, 404
        x = dao.get_message(id)
        if x is None:
            return None, 404
        x['timestamp'] = common.str_from_date(x['timestamp'])
        return x, 200


class TopicRes(Resource):
    def get(self, topic):
        if not val_topic(topic):
            return None, 404
        x = dao.get_messages_with(topic)
        if x is None:
            return None, 404
        return x, 200


class CleanRes(Resource):
    def post(self):
        dao.clean()
        return None, 200


api.add_resource(PostChirpRes, f'/{basePath}/chirp')
api.add_resource(GetChirpRes, f'/{basePath}/chirp/<string:id>')
api.add_resource(TopicRes, f'/{basePath}/topics/<string:topic>')
api.add_resource(CleanRes, f'/{basePath}/clean')

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
