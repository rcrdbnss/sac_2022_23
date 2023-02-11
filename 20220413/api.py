from flask import Flask, request
from flask_restful import Resource, Api

from cars import Cars

app = Flask(__name__, static_url_path='/static', static_folder='static')

api = Api(app)
basePath = 'api/v1'
dao = Cars()


def val_car_id(car_id) -> bool:
	return isinstance(car_id, str)


def val_car_data(data) -> bool:
	for k in ['make', 'model', 'cc', 'cv', 'engine', 'price', 'used']:
		if k not in data.keys():
			return False

	if not isinstance(data['make'], str):
		return False
	if len(data['make']) < 3:
		return False

	if not isinstance(data['model'], str):
		return False
	if len(data['model']) < 3:
		return False

	if not isinstance(data['cc'], int):
		return False

	if not isinstance(data['cv'], int):
		return False
	if data['cv'] < 59:
		return False

	if not isinstance(data['engine'], str):
		return False
	if data['engine'] not in ['diesel', 'petrol', 'hybrid', 'electric']:
		return False

	if not isinstance(data['price'], float):
		if isinstance(data['price'], int):
			data['price'] = float(data['price'])
		else:
			return False

	if not isinstance(data['used'], bool):
		return False

	return True


def val_user_data(data) -> bool:
	for k in ['name', 'surname', 'email', 'selling']:
		if k not in data.keys():
			return False

	for k in ['name', 'surname', 'email']:
		if not isinstance(data[k], str):
			return False

	if not isinstance(data['selling'], list):
		return False
	for selling in data['selling']:
		for k in ['car_id', 'car_details']:
			if k not in selling.keys():
				return False
		if not isinstance(selling['car_id'], str):
			return False
		if not val_car_data(selling['car_details']):
			return False

	return True


class CarRes(Resource):
	def get(self, car_id):
		if not val_car_id(car_id):
			return None, 404
		c = dao.get_car(car_id)
		if c is None:
			return None, 404
		return c, 200

	def post(self, car_id):
		if not val_car_id(car_id):
			return None, 400
		data = request.json
		if not val_car_data(data):
			return None, 400
		if dao.get_car(car_id) is not None:
			return None, 409
		dao.add_car(car_id, **data)
		return None, 201


class UserRes(Resource):
	def post(self):
		data = request.json
		if not val_user_data(data):
			return None, 400

		selling_ids = []
		selling_new = data['selling']  # [ { car_id: uuid, car_details: {} } ]
		for sn in selling_new:
			if dao.get_car(sn['car_id']) is not None:
				return None, 409
			dao.add_car(sn['car_id'], **sn['car_details'])
			selling_ids.append(sn['car_id'])

		u = dao.get_user(data['email'])
		if u is not None:
			for s in u['selling']: #.keys():  # { uuid: ref }
				selling_ids.append(s)

		data['selling'] = list(set(selling_ids))
		dao.add_user(**data)
		return None, 201


api.add_resource(CarRes, f'/{basePath}/car/<string:car_id>')
api.add_resource(UserRes, f'/{basePath}/user/selling')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
