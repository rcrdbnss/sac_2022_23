from flask import Flask, request
from flask_restful import Api, Resource

import common
from dao import DAO

app = Flask(__name__)

api = Api(app)
basePath = 'api/v1'
dao = DAO()


def val_body(data):
	if 'value' not in data.keys():
		return False

	value = data['value']
	if not isinstance(value, int):
		return False
	if value < 0:
		return False
	return True


class Res(Resource):
	def get(self, date: str):
		date = common.date_from_str(date)
		if not date:
			return None, 400
		x = dao.get_read(date)
		if x is None:
			return None, 400
		return x, 200

	def post(self, date: str):
		date = common.date_from_str(date)
		if not date:
			return None, 400
		data = request.json
		if not val_body(data):
			return None, 400
		if dao.get_read_if_exists(date) is not None:
			return None, 409
		dao.add_read(date, **data)
		return dao.get_read(date), 201


class CleanRes(Resource):
	def get(self):
		dao.clean()
		return None, 200


api.add_resource(Res, f'/{basePath}/consumi/<string:date>')
api.add_resource(CleanRes, f'/{basePath}/clean')

if __name__ == '__main__':
	app.run('127.0.0.1', port=8080, debug=True)
