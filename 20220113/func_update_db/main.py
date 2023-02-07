#!/usr/bin/python3
from google.cloud import firestore


def update_db(data, context):
	db = firestore.Client()
	doc = data['value']['fields']
	slot = doc['slot']['integerValue']
	quantity = doc['quantity']['integerValue']
	slot_doc = db.collection('slots').document(slot)
	slot_dict = slot_doc.get().to_dict()
	slot_old_qty = int(slot_dict['quantity'])
	slot_doc.update({'quantity': slot_old_qty - int(quantity)})
	slot_min = int(slot_dict['minimum'])
	if slot_old_qty - int(quantity) < slot_min:
		db.collection('wine_restocks').document(slot).set({
			'quantity': 6
		})
