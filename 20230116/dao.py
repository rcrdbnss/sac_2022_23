import json
import numpy as np
from datetime import datetime
from google.cloud import firestore


class DAO:

	def __init__(self):
		self.__db = firestore.Client()
		self.__col = self.__db.collection('readings')
		self.__in_date_fmt = '%Y%m%d'

		self.__dates = []
		for doc in self.__col.list_documents():
			self.__dates.append(datetime.strptime(doc.id, self.__in_date_fmt))
		self.__dates = set(self.__dates)

	def add(self, date: datetime, value: int):
		date_ = date.strftime(self.__in_date_fmt)
		self.__col.document(date_).set({
			"value": value,
			"isInterpolated": False
		})
		self.__dates.add(date)

	def get_last_dates(self, date: datetime, n=1):
		arr = np.array(list(self.__dates))
		arr = np.sort(arr[arr < date])
		n_ = np.min([len(arr), n])
		return arr[-n_:]

	def get_if_exists(self, date: datetime):
		date_ = date.strftime(self.__in_date_fmt)
		doc = self.__col.document(date_).get()
		return doc.to_dict() if doc.exists else None

	def get(self, date: datetime):
		doc = self.get_if_exists(date)
		if doc is not None:
			return doc
		else:
			rx = 0
			ld = self.get_last_dates(date, 2)
			if len(ld) == 2:
				d1, d2 = ld
				r1 = self.get_if_exists(d1)['value']
				r2 = self.get_if_exists(d2)['value']
				rx = r2 + (r2 - r1) / (d2 - d1).total_seconds() * (date - d2).total_seconds()
			elif len(ld) == 1:
				rx = ld[0]
			return {
				'value': rx,
				'isInterpolated': True
			}

	def clean(self):
		for d in self.__col.list_documents():
			d.delete()


if __name__ == '__main__':
	date_fmt = "%d-%m-%Y"
	dao = DAO()
	# dao.clean()
	with open('data.json') as f:
		data = json.load(f)
	for k, v in data.items():
		dao.add(datetime.strptime(k, date_fmt), **v)

	print(dao.get(datetime.strptime("10-01-2023", date_fmt)))
	print(dao.get(datetime.strptime("15-02-2023", date_fmt)))
	print(dao.get_last_dates(datetime.strptime("15-02-2023", date_fmt), 10))
