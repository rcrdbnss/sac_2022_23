from datetime import datetime

from flask import Flask, request
from flask_restful import Resource, Api

from plants import Plants

app = Flask(__name__, static_url_path='/static', static_folder='static')

api = Api(app)
basePath = 'api/v1'
dao = Plants()


def validate_date(date: str) -> bool:
	try:
		datetime.strptime(date, '%Y-%m-%d')
		return True
	except:
		return False


def validate_plant_name(plant_name: str) -> bool:
	return 3 <= len(plant_name) <= 20


def validate_planted_info(data) -> bool:
	for k in ['plant', 'num']:
		if k not in data.keys():
			return False

	if not isinstance(data['num'], int):
		return False
	if data['num'] < 1:
		return False

	return validate_plant_details(data['plant'])


def validate_plant_details(data) -> bool:
	for k in ['name', 'sprout-time', 'full-growth', 'edible']:
		if k not in data.keys():
			return False

	if not isinstance(data['name'], str):
		return False
	if len(data['name']) < 3:
		return False

	if not isinstance(data['sprout-time'], str):
		return False
	if len(data['sprout-time']) < 3:
		return False

	if not isinstance(data['full-growth'], str):
		return False
	if len(data['full-growth']) < 5:
		return False

	if not isinstance(data['edible'], bool):
		return False

	return True


class PlantRes(Resource):
	def get(self, date, plant):
		if not validate_date(date):
			return None, 404
		if not validate_plant_name(plant):
			return None, 404
		p = dao.get(date, plant)
		if p is None:
			return None, 404
		return p, 200

	def post(self, date, plant):
		if not validate_date(date):
			return None, 400
		if not validate_plant_name(plant):
			return None, 400
		data = request.json
		if not validate_planted_info(data):
			return None, 400
		if plant != data['plant']['name']:
			return None, 400
		if dao.get(date, plant) is not None:
			return None, 409
		dao.add(date, **data)
		return None, 201


class PlantInfoRes(Resource):
	def get(self, date, plant, field):
		if not validate_date(date):
			return None, 404
		if not validate_plant_name(plant):
			return None, 404
		if field not in ['sprout-time', 'full-growth', 'edible']:
			return False
		p = dao.get(date, plant)
		if p is None:
			return None, 404
		print(p)
		return str(p['plant'][field]), 200


api.add_resource(PlantRes, f'/{basePath}/garden/plant/<string:date>/<string:plant>')
api.add_resource(PlantInfoRes, f'/{basePath}/garden/plant/<string:date>/<string:plant>/<string:field>')
if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
