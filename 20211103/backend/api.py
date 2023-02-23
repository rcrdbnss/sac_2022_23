import common
from dao import DAO
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)
basePath = 'api/v1'
dao = DAO()


def val_body(data):
    for k in ['name', 'extraction-date', 'partecipants']:
        if k not in data.keys():
            return False

    name = data['name']
    if not isinstance(name, str):
        return False

    extraction_date = data['extraction-date']
    if not isinstance(extraction_date, str):
        return False
    if not common.date_from_str(extraction_date):
        return False

    partecipants = data['partecipants']
    if not isinstance(partecipants, list):
        return False
    for p in partecipants:
        if not isinstance(p, str):
            return False

    return True


class CreateSantaRes(Resource):
    def post(self, email):
        if not common.is_email(email):
            return None, 400
        data = request.json
        if not val_body(data):
            return None, 400
        if len(dao.get_created_by(email)) >= 2:
            return None, 412
        data['extraction_date'] = common.date_from_str(data['extraction-date'])
        dao.add(email, **data)
        return None, 201


class GenerateRes(Resource):
    def get(self, santa_id):
        id = common.uuid_from_str(santa_id)
        if not id:
            return None, 404
        x = dao.get(id)
        if x is None:
            return None, 404
        return x, 200


class CleanRes(Resource):
    def get(self):
        dao.clean()
        return None, 200


api.add_resource(CreateSantaRes, f'/{basePath}/create_santa/<string:email>')
api.add_resource(GenerateRes, f'/{basePath}/generate/<string:santa_id>')
api.add_resource(CleanRes, f'/{basePath}/clean')

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)
