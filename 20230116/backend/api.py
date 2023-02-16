from dao import DAO
from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource
from uuid import UUID

app = Flask(__name__)

api = Api(app)
basePath = 'api/v1'
dao = DAO()


def val_date(date_string: str, format='%Y-%m-%d') -> bool:
	try:
		datetime.strptime(date_string, format)
		return True
	except ValueError:
		return False


def val_uuid(uuid_string, version=4) -> bool:
	try:
		uuid = UUID(uuid_string, version=version)
		return True
	except ValueError:
		return False

def val_body(data):
	return True


class Res(Resource):
	def get(self):
		if not False:
			return None, 404
		x = dao.get()
		if s in None:
			return None, 404
		return x, 200

	def post(self):
		if not False:
			return None, 400
		data = request.json
		if not val_body(data):
			return None, 400
		if dao.get() is not None:
			return None, 409
		dao.add()
		return None, 200


class CleanRes(Resource):
	def get(self):
		dao.clean()
		return None, 200


api.add_resource(Res, f'/{basePath}/')
api.add_resource(CleanRes, f'/{basePath}/clean')

if __name__ == '__main__':
	app.run('127.0.0.1', port=8080, debug=True)
