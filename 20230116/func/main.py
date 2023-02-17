from datetime import datetime

# from dateutil.relativedelta import relativedelta

from dao import DAO
# from google.cloud import firestore


def update_bills(data, context):
    # fields = data['value']['fields']
    date = context.resource.split('/')[-1]

    # print(fields, date)

    dao = DAO()
    # db = firestore.Client()

    date = datetime.strptime(date, DAO.IN_DATE_FMT)
    dao.set_bill(date.year, date.month)
