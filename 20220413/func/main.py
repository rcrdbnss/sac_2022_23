import json

from google.cloud import firestore, pubsub_v1


def check_prices(data, context):
	db = firestore.Client()
	pub = pubsub_v1.PublisherClient()
	topic_path = pub.topic_path('rbenassi-20220413', 'cheaper_cars')

	print('data', data)  # debug
	user_id = context.resource.split('/')[-1]
	fields = data['value']['fields']  # user just upserted
	print('fields', fields, user_id)  # debug
	selling = fields['selling']['arrayValue']['values']
	for s in selling:
		car_id = s['stringValue']
		car = db.collection('cars').document(car_id).get().to_dict()
		col = db.collection('cars')
		for f in ['make', 'model', 'cc', 'cv', 'engine', 'used']:
			col = col.where(f, '==', car[f])
		for doc in col.where('price', '>', car['price']).stream():
			for u in db.collection('users').where('selling', 'array_contains', doc.id).stream():  # should be one and only one
				to_pub = {
					'user_to_warn': u.id,
					'car_to_warn': doc.id,
					'user_cheaper': user_id,
					'car_cheaper': car_id
				}
				print('result', to_pub, pub.publish(topic_path, json.dumps(to_pub).encode('utf-8')).result())
