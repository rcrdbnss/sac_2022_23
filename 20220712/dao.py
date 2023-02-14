import json

from google.cloud import firestore

lanes_order = [4, 5, 3, 6, 2, 7, 1, 8]


def field(s: str):
	return f"_{s.replace('-', '_')}"


class DAO:

	def __set_date_time_cnt(self, date, time):
		if date not in self.date_time_cnt.keys():
			self.date_time_cnt[date] = {}
		time_cnt = self.date_time_cnt[date]
		if time not in time_cnt.keys():
			time_cnt[time] = 0

	def __init__(self):
		self.db = firestore.Client()
		self.col = 'pool_rsvs'
		self.date_time_cnt = {}

		for user in self.db.collection(self.col).stream():
			user = user.to_dict()
			for date_ in user.keys():
				for time_ in user[date_].keys():
					v = user[date_][time_]
					date = v['date']
					time = v['time']
					self.__set_date_time_cnt(date, time)
					self.date_time_cnt[date][time] += 1

	def add(self, user, date, time, others=None) -> bool:
		self.__set_date_time_cnt(date, time)
		time_cnt = self.date_time_cnt[date]
		if time_cnt[time] >= 16:
			return False

		lane = lanes_order[time_cnt[time]]
		self.db.collection(self.col).document(user).set({
			field(date): {
				field(time): {
					'date': date,
					'time': time,
					'lane': lane
				}
			}
		}, merge=True)
		time_cnt[time] += 1
		if others is not None:
			for o in others:
				if not self.add(user, **o):
					return False

		return True

	def get_ud_rsvs(self, user, date):
		date_ = field(date)
		doc = self.db.collection(self.col).document(user).get([field(date)])
		if doc.exists:
			doc = doc.to_dict()[date_]
			ret = []
			for time_ in doc:
				ret.append(doc[time_])
			return ret if len(ret) > 0 else None
		else:
			return None

	def get_dt_rsvs(self, date, time):
		date_ = field(date)
		time_ = field(time)
		rsvs = {}
		for l in sorted(lanes_order):
			# rsvs[l] = 0
			rsvs[l] = []
		for doc in self.db.collection(self.col).where(f'{date_}.{time_}', '!=', False).stream():
			lane = doc.get(f'{date_}.{time_}.lane')
			# rsvs[lane] += 1
			rsvs[lane].append(doc.id)
		ret = []
		for k, v in rsvs.items():
			dc = {
				'lane': k,
				'n_users': v
			}
			ret.append(dc)
		return ret

	def get_users(self, date, time, lane):
		date_ = field(date)
		time_ = field(time)
		users = []
		for doc in self.db.collection(self.col).where(f'{date_}.{time_}.lane', '==', lane).stream():
			users.append(doc.id)
		return users

	def clean(self):
		for d in self.db.collection(self.col).list_documents():
			d.delete()


if __name__ == '__main__':
	dao = DAO()
	dao.clean()
	with open('data.json') as f:
		data = json.load(f)
	for user in data.keys():
		for date in data[user].keys():
			dao.add(user, date, **data[user][date])

	print(dao.get_ud_rsvs("001", "2023-02-10"))
	print(dao.get_dt_rsvs("2023-02-10", "08-10"))
	print(dao.get_users("2023-02-10", "08-10", 3))
