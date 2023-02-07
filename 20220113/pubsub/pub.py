import json
import os, sys
from google.cloud import pubsub_v1

pub = pubsub_v1.PublisherClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-sac-20220113'
topic = os.environ['TOPIC'] if os.environ['TOPIC'] else 'wine_orders'
topic_path = pub.topic_path(prjid, topic)


def order(slot: int, quantity=1):
	data = {
		'slot': slot,
		'quantity': quantity
	}
	res = pub.publish(topic_path, json.dumps(data).encode('utf-8'))
	print(data, res.result())


if __name__ == '__main__':
	slot = int(sys.argv[1])
	quantity = 1
	if len(sys.argv) >= 3:
		quantity = int(sys.argv[2])
	order(slot, quantity)
