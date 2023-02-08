import json

from google.cloud import firestore


class Plants:

	def __init__(self):
		self.__db = firestore.Client()
		self.slots = {}
		self.__populate_db('plants.json')

	def add(self, date, plant, num):
		plant_name = plant['name'].replace(" ", "_")
		self.__db.collection('plants').document(date).set({
			plant_name: {
				'plant': plant,
				'num': num
			}
		}, merge=True)

	def __populate_db(self, filename):
		with open(filename) as f:
			data = json.load(f)
		for k in data.keys():
			self.add(k, **data[k])

	def get(self, date, plant_name):
		plant_name = plant_name.replace(" ", "_")
		p = self.__db.collection('plants').document(date).get([plant_name])
		return p.to_dict()[plant_name] if p.exists else None

	def get_all(self):
		ret = {}
		for doc in self.__db.collection('plants').stream():
			ret[doc.id] = doc.to_dict()
		return ret


if __name__ == '__main__':
	p = Plants()
	print(p.get("2021-02-09", "Chili Pepper"))
	print(p.get_all())
