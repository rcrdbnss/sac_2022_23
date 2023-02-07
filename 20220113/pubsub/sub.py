import json
import os
from datetime import datetime

from google.cloud import firestore, pubsub_v1

sub = pubsub_v1.SubscriberClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-sac-20220113'
subsc = os.environ['SUBSCRIPTION_NAME'] if os.environ['SUBSCRIPTION_NAME'] else 'wine_sub'
subsc_path = sub.subscription_path(prjid, subsc)

db = firestore.Client()


def callback(message):
	message.ack()
	data = json.loads(message.data.decode('utf-8'))
	db.collection('wine_orders').document(str(datetime.now())).set(data)
	print(data)


if __name__ == '__main__':
	pull = sub.subscribe(subsc_path, callback=callback)
	try:
		pull.result(timeout=30)
	except:
		pull.cancel()
