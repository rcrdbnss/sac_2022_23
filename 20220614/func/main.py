#!/usr/bin/python3
import json

from google.cloud import firestore


def charts(data, context):
	db = firestore.Client()

	# print('data:', data)
	# print('context:', context)
	fields = data['value']['fields']
	league = context.resource.split('/')[-1]

	calculate_chart_(db, fields, league, 'group_a')
	calculate_chart_(db, fields, league, 'group_b')


def calculate_chart_(db, fields, league, group):
	scores = fields[group]['mapValue']['fields']
	# print(group, 'scores:', scores)
	if len(scores) == 6:
		matches = db.collection('leagues').document(league).get([group]).to_dict()[group]
		# print(group, 'matches:', matches)

		chart = {}
		for i in scores.keys():
			team0 = matches[i][0]
			team1 = matches[i][1]
			if team0 not in chart.keys():
				chart[team0] = 0
			if team1 not in chart.keys():
				chart[team1] = 0
			score0 = scores[i]['arrayValue']['values'][0]['integerValue']
			score1 = scores[i]['arrayValue']['values'][1]['integerValue']
			if score0 > score1:
				chart[team0] += 3
			elif score0 < score1:
				chart[team1] += 3
			else:
				chart[team0] += 1
				chart[team1] += 1
		# print('chart:', chart)
		db.collection('charts').document(league).set({
			group: chart
		})


class Ctx:
	def __init__(self, resource):
		self.resource = resource


if __name__ == '__main__':
	with open('data.json') as f:
		data = json.load(f)
		context = Ctx("projects/rbenassi-20220614/databases/(default)/documents/scores/G7League")
		charts(data, context)
