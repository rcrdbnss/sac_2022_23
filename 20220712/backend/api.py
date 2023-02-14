from dao import DAO
from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)
basePath = 'api/v1'
dao = DAO()


def val_user(uuid):
	return True


def val_date(date_string: str, format='%Y-%m-%d') -> bool:
	try:
		datetime.strptime(date_string, format)
		return True
	except:
		return False


def val_time(time):
	return time in ['08-10', '10-12', '12-14', '14-16', '16-18', '18-20']


def val_rsv_item(data):
	for k in ['date', 'time']:
		if k not in data.keys():
			return False

	if 'lane' in data.keys():
		return False

	date = data['date']
	if not isinstance(date, str):
		return False
	if not val_date(date):
		return False

	time = data['time']
	if not isinstance(time, str):
		return False
	if not val_time(time):
		return False

	return True


def val_booking_data(data):
	if 'time' not in data.keys():
		return False

	if 'lane' in data.keys():
		return False

	time = data['time']
	if not isinstance(time, str):
		return False
	if not val_time(time):
		return False

	if 'others' in data.keys():
		others = data['others']
		if not isinstance(others, list):
			return False
		for o in others:
			if not val_rsv_item(o):
				return False

	return True


class PoolBookingRes(Resource):
	def get(self, user, date):
		if not val_user(user):
			return None, 404
		if not val_date(date):
			return None, 404
		x = dao.get(user, date)
		if x is None:
			return None, 404
		details = []
		for time in x.keys():
			details.append({
				'date': date,
				'time': time,
				'lane': x[time]
			})
		return details, 200

	def post(self, user, date):
		if not val_user(user):
			return None, 404
		if not val_date(date):
			return None, 404
		data = request.json
		if not val_booking_data(data):
			return None, 404
		x = dao.get(user, date)
		if x is not None:
			if data['time'] in x.keys():
				return None, 409
		if not dao.add(user, date, **data):
			return None, 412
		return dao.get(user, date), 201

api.add_resource(PoolBookingRes, f'/{basePath}/pool/<string:user>/<string:date>')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
