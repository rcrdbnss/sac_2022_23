import json
import os
import sys

from google.cloud import pubsub_v1

pub = pubsub_v1.PublisherClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-20220614'
topic = os.environ['TOPIC'] if os.environ['TOPIC'] else 'scores'
topic_path = pub.topic_path(prjid, topic)

if __name__ == '__main__':
	league = sys.argv[1]
	group = sys.argv[2]
	match = sys.argv[3]
	score1 = sys.argv[4]
	score2 = sys.argv[5]

	data = {
		'league': league,
		'group': group,
		'match': match,
		'score1': int(score1),
		'score2': int(score2)
	}

	res = pub.publish(topic_path, json.dumps(data).encode('utf-8'))
	print(data, res.result())
