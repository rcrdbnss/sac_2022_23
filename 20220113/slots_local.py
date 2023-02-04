import json


class Slots:

	def __init__(self):
		self.slots = {}
		self.__populate_db('slots.json')

	def add(self, n, name, type, producer, year, price, quantity, minimum):
		self.slots[n] = {
			'label': {
				'name': name,
				'type': type,
				'producer': producer,
				'year': year,
				'price': price,
			},
			'quantity': quantity,
			'minimum': minimum
		}

	def __populate_db(self, filename):
		with open(filename) as f:
			self.slots = json.load(f)

	def get(self, n):
		if n in self.slots.keys():
			return self.slots[n]
		else:
			return None

	def get_all(self):
		return list(self.slots.keys())

	def delete(self, n):
		if n is self.slots.keys():
			del self.slots[n]

	def clean(self):
		self.slots = {}


if __name__ == '__main__':
	s = Slots()
	print(s.get_all())
	print(s.get("0"))
