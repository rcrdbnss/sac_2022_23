import json
import os
import sys

from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

sub = pubsub_v1.SubscriberClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-20230223'


def callback(message):
	message.ack()
	print(json.loads(message.data.decode('utf-8')))


if __name__ == '__main__':
	hashtag = sys.argv[1]
	hashtag = hashtag.replace("#", "").lower()
	topic_path = sub.topic_path(prjid, hashtag)
	subsc_path = sub.subscription_path(prjid, f'{hashtag}_sub')

	with sub:
		try:
			subscription = sub.create_subscription(
				request={'name': subsc_path, 'topic': topic_path}
			)
		except AlreadyExists:
			pass

		pull = sub.subscribe(subsc_path, callback=callback)
		try:
			pull.result()
		except:
			print("Cancelling...")
			pull.cancel()
