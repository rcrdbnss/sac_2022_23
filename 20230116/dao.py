import json
import numpy as np
from datetime import datetime

from dateutil.relativedelta import relativedelta
from google.cloud import firestore


class DAO:
    KWH_PRICE = 0.5
    IN_DATE_FMT = '%Y%m%d'
    HR_DATE_FMT = '%d-%m-%Y'

    def __init__(self):
        self.__db = firestore.Client()
        self.__reads_col = self.__db.collection('readings')
        self.__bills_col = self.__db.collection('bills')

        self.__read_dates = []
        for doc in self.__reads_col.list_documents():
            self.__read_dates.append(datetime.strptime(doc.id, DAO.IN_DATE_FMT))
        self.__read_dates = set(self.__read_dates)

    def add_read(self, date: datetime, value: int):
        date_ = date.strftime(DAO.IN_DATE_FMT)
        self.__reads_col.document(date_).set({
            "value": value,
            "isInterpolated": False
        })
        self.__read_dates.add(date)

    def get_last_read_dates(self, date: datetime, n=1) -> list[datetime]:
        arr = np.array(list(self.__read_dates))
        arr = np.sort(arr[arr <= date])
        n_ = np.min([len(arr), n])
        return arr[-n_:].tolist()

    def get_read_if_exists(self, date: datetime):
        date_ = date.strftime(DAO.IN_DATE_FMT)
        doc = self.__reads_col.document(date_).get()
        return doc.to_dict() if doc.exists else None

    def get_read(self, date: datetime):
        doc = self.get_read_if_exists(date)
        if doc is not None:
            return doc
        else:
            rx = 0
            ld = self.get_last_read_dates(date, 2)
            if len(ld) == 2:
                d1, d2 = ld
                r1 = self.get_read_if_exists(d1)['value']
                r2 = self.get_read_if_exists(d2)['value']
                rx = r2 + (r2 - r1) / (d2 - d1).total_seconds() * (date - d2).total_seconds()
            elif len(ld) == 1:
                rx = self.get_read_if_exists(ld[0])['value']
            return {
                'value': rx,
                'isInterpolated': True
            }

    def set_bill_by_ref_month(self, year: int, month: int):
        """
        Args:
            year: anno di riferimento (non di emissione)
            month: mese di riferimento (non di emissione)
        """
        start_date = datetime(year=year, month=month, day=1)
        emit_date = start_date + relativedelta(months=1)
        end_date = start_date + relativedelta(days=-1)
        last_read_date = self.get_last_read_dates(end_date)[0]

        start_read = self.get_read(start_date)['value']
        end_read = self.get_read(end_date)['value']

        month_consum = end_read - start_read
        amount = month_consum * DAO.KWH_PRICE
        self.__bills_col.document(emit_date.strftime(DAO.IN_DATE_FMT)).set({
            'amount': amount,
            'start_date': start_date.strftime(DAO.HR_DATE_FMT),
            'end_date': end_date.strftime(DAO.HR_DATE_FMT),
            'last_read_date': last_read_date.strftime(DAO.HR_DATE_FMT),
            'month_consum': month_consum
        })

    def get_bills(self):
        bills = []
        for doc in self.__bills_col.stream():
            bills.append(datetime.strptime(doc.id, DAO.IN_DATE_FMT))
        return bills

    def get_bill_by_ref_month(self, year: int, month: int):
        """
        Args:
            year: anno di riferimento (non di emissione)
            month: mese di riferimento (non di emissione)
        Returns:

        """
        self.set_bill_by_ref_month(year, month)
        start_date = datetime(year=year, month=month, day=1)
        emit_date = start_date + relativedelta(months=1)
        return self.get_bill_by_emit_date(emit_date)

    def get_bill_by_emit_date(self, emit_date: datetime):
        return self.__bills_col.document(emit_date.strftime(DAO.IN_DATE_FMT)).get().to_dict()

    def clean(self):
        for d in self.__reads_col.list_documents():
            d.delete()
        for d in self.__bills_col.list_documents():
            d.delete()


if __name__ == '__main__':
    date_fmt = "%d-%m-%Y"
    dao = DAO()
    dao.clean()
    with open('data.json') as f:
        data = json.load(f)
    for k, v in data.items():
        dao.add_read(datetime.strptime(k, date_fmt), **v)

    print(dao.get_read(datetime.strptime("10-01-2023", date_fmt)))
    print(dao.get_read(datetime.strptime("15-02-2023", date_fmt)))
    print(dao.get_last_read_dates(datetime.strptime("15-02-2023", date_fmt), 10))
