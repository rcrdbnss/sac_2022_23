import json

from google.cloud import firestore


class Slots:

	def __init__(self):
		self.__db = firestore.Client()
		self.slots = {}
		self.__populate_db('slots.json')

	def add(self, n, name, type, producer, year, price, quantity, minimum):
		self.__db.collection('slots').document(n).set({
			'label': {
				'name': name,
				'type': type,
				'producer': producer,
				'year': year,
				'price': price,
			},
			'quantity': quantity,
			'minimum': minimum
		})

	def __populate_db(self, filename):
		with open(filename) as f:
			data = json.load(f)
		for k in data.keys():
			s = data[k]
			l = s['label']
			self.add(k, l['name'], l['type'], l['producer'], l['year'], l['price'], s['quantity'], s['minimum'])

	def get(self, n):
		s = self.__db.collection('slots').document(n).get()
		return s.to_dict() if s.exists else None

	def delete(self, n):
		self.__db.collection('slots').document(n).delete()

	def clean(self):
		for d in self.__db.collection('slots').list_documents():
			d.delete()


if __name__ == '__main__':
	s = Slots()
	print(s.get("0"))
