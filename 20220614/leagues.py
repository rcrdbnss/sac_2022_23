import json

from google.cloud import firestore


def matches(teams):
	matches = []
	for t1 in teams:
		for t2 in teams:
			if t1 < t2:
				matches.append([t1, t2])
	return matches


def matches_dict(teams):
	matches = {}
	i = 0
	for t1 in teams:
		for t2 in teams:
			if t1 < t2:
				matches[str(i)] = [t1, t2]
				i += 1
	return matches


class Leagues:

	def __init__(self):
		self.db = firestore.Client()
		self.populate_db('leagues.json')

	def add(self, name, start_date, teams):
		a_teams = teams[0:4]
		b_teams = teams[4:8]
		group_a = matches_dict(a_teams)
		group_b = matches_dict(b_teams)
		data = {
			'start_date': start_date,
			'teams': teams,
			'group_a': group_a,
			'group_b': group_b,
			'finals': {
				'0': ["First_Place_A", "Second_Place_B"],
				'1': ["Second_Place_A", "First_Place_B"],
				'2': ["Winner_Semi_1", "Winner_Semi_2"]
			}
		}
		self.db.collection('leagues').document(name).set(data)

	def populate_db(self, filename):
		with open(filename) as f:
			data = json.load(f)
		for k in data.keys():
			self.add(k, **data[k])

	def get(self, name):
		l = self.db.collection('leagues').document(name).get()
		if l.exists:
			l = l.to_dict()
			for k in ['group_a', 'group_b', 'finals']:
				ls = []
				for i, v in l[k].items():
					ls.append(v)
				l[k] = ls
			return l
		else:
			return None

	def get_team(self, league_name, team):
		pass

	def add_team(self, league_name, team, captain, players):
		self.db.collection('teams').document(league_name).set({
			team: {
				'captain': captain,
				'players': players
			}
		}, merge=True)


if __name__ == '__main__':
	dao = Leagues()
	print(dao.get('SerieAMinuscola'))
