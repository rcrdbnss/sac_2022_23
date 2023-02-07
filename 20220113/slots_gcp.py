import json

from google.cloud import firestore


class Slots:

	def __init__(self):
		self.__db = firestore.Client()
		self.slots = {}
		self.__populate_db('slots.json')

	def add(self, slot_num, label, quantity, minimum):
		self.__db.collection('slots').document(slot_num).set({
			'label': label,
			'quantity': quantity,
			'minimum': minimum
		})

	def __populate_db(self, filename):
		with open(filename) as f:
			data = json.load(f)
		for k in data.keys():
			self.add(k, **data[k])

	def get(self, slot_num):
		s = self.__db.collection('slots').document(slot_num).get()
		return s.to_dict() if s.exists else None

	def get_all(self):
		return [s.to_dict() for s in self.__db.collection('slots').stream()]

	def get_type(self, type):
		if type not in ['sparkling', 'white', 'red', 'sweet']:
			return None
		return [s.to_dict() for s in self.__db.collection('slots').where('label.type', '==', type).stream()]

	def delete(self, slot_num):
		self.__db.collection('slots').document(slot_num).delete()

	def clean(self):
		for d in self.__db.collection('slots').list_documents():
			d.delete()


if __name__ == '__main__':
	s = Slots()
	print(s.get("0"))
	print(s.get_type("red"))
	new_slot = {
		'label': {
			'name': 'GibberishSweetWine',
			'type': 'sweet',
			'producer': 'MyImagination',
			'year': 2023,
			'price': 100.0
		},
		'quantity': 8,
		'minimum': 6
	}
	s.add("3", **new_slot)
