from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api

from leagues import Leagues

app = Flask(__name__)

api = Api(app)
basePath = 'api/v1'
dao = Leagues()


def validate_date(date_string: str, format='%Y-%m-%d') -> bool:
	try:
		datetime.strptime(date_string, format)
		return True
	except:
		return False


def val_league_name(name):
	return isinstance(name, str) and (5 <= len(name) <= 64)


def val_league_data(data):
	for k in ['start_date', 'teams']:
		if k not in data.keys():
			return False

	if not isinstance(data['start_date'], str):
		return False
	if not validate_date(data['start_date']):
		return False

	teams = data['teams']
	if not isinstance(teams, list):
		return False
	if len(teams) != 8:
		return False
	for t in teams:
		if not val_team_name(t):
			return False

	return True


def val_team_name(name):
	return isinstance(name, str) and (2 <= len(name) <= 64)


def val_team_data(data):
	for k in ['captain', 'players']:
		if k not in data.keys():
			return False

	players = data['players']
	player_names = []
	if not isinstance(players, list):
		return False
	for p in players:
		if not val_player_data(p):
			return False
		player_names.append(p['name'])

	captain = data['captain']
	if not isinstance(captain, str):
		return False
	if captain not in player_names:
		return False

	return True


def val_player_data(data):
	for k in ['name', 'role']:
		if k not in data.keys():
			return False

	if not isinstance(data['name'], str):
		return False
	if not isinstance(data['role'], str):
		return False

	return True


class LeagueRes(Resource):
	def get(self, name):
		if not val_league_name(name):
			return None, 404
		l = dao.get(name)
		if l is None:
			return None, 404
		ret = {}
		# skip 'teams'
		for k in ['start_date', 'group_a', 'group_b', 'finals']:
			ret[k] = l[k]
		return ret, 200

	def post(self, name):
		if not val_league_name(name):
			return None, 400
		data = request.json
		if not val_league_data(data):
			return None, 400
		if dao.get(name) is not None:
			return None, 409
		dao.add(name, **data)
		return dao.get(name), 201


class TeamRes(Resource):
	def post(self, name, team):
		if not val_league_name(name):
			return None, 400
		if not val_team_name(team):
			return None, 400
		l = dao.get(name)
		if team not in l['teams']:
			return None, 400
		data = request.json
		if not val_team_data(data):
			return None, 400
		if dao.get_team(name, team) is not None:
			return None, 409
		dao.add_team(name, team, **data)
		return None, 201


api.add_resource(LeagueRes, f'/{basePath}/league/<string:name>')
api.add_resource(TeamRes, f'/{basePath}/league/<string:name>/<string:team>')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)
