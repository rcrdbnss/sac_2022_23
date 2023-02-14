import json

from google.cloud import firestore

lanes_order = [4, 5, 3, 6, 2, 7, 1, 8]

class DAO:

	def __set_date_time_cnt(self, date, time):
		if date not in self.date_time_cnt.keys():
			self.date_time_cnt[date] = {}
		time_cnt = self.date_time_cnt[date]
		if time not in time_cnt.keys():
			time_cnt[time] = 0

	def __init__(self):
		self.db = firestore.Client()
		self.col = 'pool_bookings'
		self.date_time_cnt = {}

		for user in self.db.collection(self.col).stream():
			user = user.to_dict()
			# print(user)
			for date in user.keys():
				for time in user[date].keys():
					self.__set_date_time_cnt(date, time)
					self.date_time_cnt[date][time] += 1

	def add(self, user, date, time, others=None) -> bool:
		self.__set_date_time_cnt(date, time)
		time_cnt = self.date_time_cnt[date]
		if time_cnt[time] >= 16:
			return False

		lane = lanes_order[time_cnt[time]]
		self.db.collection(self.col).document(user).set({
			date: {
				# time: {
				# 	'lane': lane
				# }
				time: lane
			}
		}, merge=True)
		time_cnt[time] += 1
		if others is not None:
			for o in others:
				if not self.add(user, **o):
					return False

		return True

	def get(self, user, date):
		doc = self.db.collection(self.col).document(user).get()
		if doc.exists:
			doc = doc.to_dict()
			return doc[date] if date in doc.keys() else None
		else:
			return None

	def clean(self):
		for d in self.db.collection(self.col).list_documents():
			d.delete()


if __name__ == '__main__':
	dao = DAO()
	with open('data.json') as f:
		data = json.load(f)
	for user in data.keys():
		for date in data[user].keys():
			dao.add(user, date, **data[user][date])

	print(dao.get("001", "2023-02-10"))
