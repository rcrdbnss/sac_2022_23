import json
import os
import sys

from google.cloud import pubsub_v1

pub = pubsub_v1.PublisherClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-20220712'
topic = os.environ['TOPIC'] if os.environ['TOPIC'] else 'bracelet_req'
topic_path = pub.topic_path(prjid, topic)

if __name__ == '__main__':
	user = sys.argv[1]
	date = sys.argv[2]
	time = sys.argv[3]

	data = {
		'user': user,
		'date': date,
		'time': time
	}

	res = pub.publish(topic_path, json.dumps(data).encode('utf-8'))
	print(data, res.result())
