from dao import DAO
from google.cloud import firestore


def check_for_rsv(data, context):
    fields = data['value']['fields']
    user = context.resource.split('/')[-1]

    print(fields, user)

    dao = DAO()
    db = firestore.Client()
