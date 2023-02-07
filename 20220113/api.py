from flask import Flask, request
from flask_restful import Resource, Api

from slots import Slots

app = Flask(__name__, static_url_path='/static', static_folder='static')

api = Api(app)
basePath = 'api/v1'
dao = Slots()


def validate_slot(data):
	for k in ['label', 'quantity', 'minimum']:
		if k not in data.keys():
			return False

	if not isinstance(data['quantity'], int):
		return False
	if data['quantity'] < 6 or data['quantity'] > 14:
		return False

	if not isinstance(data['minimum'], int):
		return False
	if data['minimum'] < 3 or data['minimum'] > 8:
		return False

	return validate_label(data['label'])


def validate_label(label_data):
	for k in ['name', 'type', 'producer', 'year', 'price']:
		if k not in label_data.keys():
			return False

	if not isinstance(label_data['name'], str):
		return False

	if not isinstance(label_data['type'], str):
		return False
	if label_data['type'] not in ['sparkling', 'white', 'red', 'sweet']:
		return False

	if not isinstance(label_data['producer'], str):
		return False

	if not isinstance(label_data['year'], int):
		return False
	if 1900 > label_data['year'] or label_data['year'] > 2021:
		return False

	if not isinstance(label_data['price'], float):
		return False
	if label_data['price'] < 0:
		return False

	return True


def validate_slot_num(slot_num):
	try:
		n = int(slot_num)
		return 0 <= n <= 9
	except:
		return False


class CleanResource(Resource):
	def get(self):
		dao.clean()
		return None, 200


class SlotResource(Resource):
	def get(self, slot_num):
		if not validate_slot_num(slot_num):
			return None, 404
		s = dao.get(slot_num)
		if s is None:
			return None, 404
		return s, 200

	def post(self, slot_num):
		if not validate_slot_num(slot_num):
			return None, 400
		data = request.json
		if not validate_slot(data):
			return None, 400
		if dao.get(slot_num) is not None:
			return None, 409
		dao.add(slot_num, **data['label'])
		return None, 201


class LabelsListResource(Resource):
	def get(self, type):
		ls = dao.get_type(type)
		if ls is None:
			return None, 404
		return [l['label'] for l in ls], 200


api.add_resource(SlotResource, f'/{basePath}/slot/<string:slot_num>')
api.add_resource(LabelsListResource, f'/{basePath}/labels/<string:type>')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
