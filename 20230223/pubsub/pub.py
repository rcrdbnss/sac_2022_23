import json
import os
import sys

from google.cloud import pubsub_v1

pub = pubsub_v1.PublisherClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-20230223'
prjpath = f'projects/{prjid}'
# topic = os.environ['TOPIC'] if os.environ['TOPIC'] else 'bracelet_req'
# topic_path = pub.topic_path(prjid, topic)

if __name__ == '__main__':
	for topic in pub.list_topics(request={"project": prjpath}):
		print(topic)
