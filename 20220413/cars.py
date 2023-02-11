import json

from google.cloud import firestore


class Cars:

	def __init__(self):
		self.db = firestore.Client()
		self.populate_db('cars.json', 'users.json')

	def add_car(self, car_id, make, model, cc, cv, engine, price, used):
		self.db.collection('cars').document(car_id).set({
			'make': make,
			'model': model,
			'cc': cc,
			'cv': cv,
			'engine': engine,
			'price': price,
			'used': used
		})

	def add_user(self, email, name, surname, selling: list):
		# selling_refs = {}
		selling_refs = []
		for s in selling:
			c = self.get_car_ref(s)
			if c.get().exists:
				# selling_refs[s] = c
				selling_refs.append(c)

		self.db.collection('users').document(email).set({
			'name': name,
			'surname': surname,
			'selling': selling
		})

	def populate_db(self, cars_file, users_file):
		with open(cars_file) as f:
			data = json.load(f)
		for k in data.keys():
			self.add_car(k, **data[k])

		with open(users_file) as f:
			data = json.load(f)
		for k in data.keys():
			self.add_user(k, **data[k])

	def get_car_ref(self, car_id):
		return self.db.collection('cars').document(car_id)

	def get_car(self, car_id):
		c = self.db.collection('cars').document(car_id).get()
		return c.to_dict() if c.exists else None

	def get_user(self, email):
		c = self.db.collection('users').document(email).get()
		return c.to_dict() if c.exists else None

	def get_makers(self):
		makers = []
		for doc in self.db.collection('cars').stream():
			makers.append(doc.to_dict()["make"])
		return list(set(makers))

	def query(self, make, max_cv, max_price, used):
		col = self.db.collection('cars')
		if make:
			col = col.where('make', '==', make)
			print(make)
		if max_cv:
			# col = col.where('cv', '<=', max_cv)
			col = col.where('cv', '==', max_cv)
		if max_price:
			# col = col.where('price', '<=', max_price)
			col = col.where('price', '==', max_price)
		if used:
			col = col.where('used', '==', used)
			print(used)
		cars = {}
		for doc in col.stream():
			cars[doc.id] = doc.to_dict()
		return cars


if __name__ == '__main__':
	c = Cars()
	print(c.get_car("111"))
	print(c.get_user("johndoe@gmail.com"))
	print(c.get_makers())
