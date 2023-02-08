import json
import os
import sys

from google.cloud import pubsub_v1

HAND_IRR = 'hand_irr'
HUMIDITY = 'humidity'

publisher = pubsub_v1.PublisherClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'myprj'


def hand_irr(seconds: str):
	topic_path = publisher.topic_path(prjid, HAND_IRR)
	data = {
		'seconds': int(seconds)
	}
	res = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))
	print(res.result())


def humidity(humidity_pct: str):
	topic_path = publisher.topic_path(prjid, HUMIDITY)
	data = {
		'humidity': float(humidity_pct)
	}
	res = publisher.publish(topic_path, json.dumps(data).encode('utf-8'))
	print(res.result())


if __name__ == '__main__':
	if sys.argv[1] == HAND_IRR:
		hand_irr(sys.argv[2])
	elif sys.argv[1] == HUMIDITY:
		humidity(sys.argv[2])
	else:
		print("ERROR! Unrecognized", sys.argv[1])
