from datetime import datetime

from dao import DAO
from google.cloud import firestore


def check_for_rsv(data, context):
	fields = data['value']['fields']
	user = context.resource.split('/')[-1]

	print(fields, user)
	user = fields['user']['stringValue']
	date = fields['date']['stringValue']
	time = fields['time']['stringValue']

	dao = DAO()
	db = firestore.Client()
	msg = {
		'user': user,
		'date': date,
		'time': time
	}
	if dao.get_udt_rsv(user, date, time) is None:
		msg['msg'] = "Denied!"
	else:
		msg['msg'] = 'Welcome!'
	print(msg)
	db.collection('display_msgs').document(user).set({
		str(datetime.now().timestamp()): msg
	})
