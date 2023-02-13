import json
import os

from google.cloud import pubsub_v1

sub = pubsub_v1.SubscriberClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-20220614'
subsc = os.environ['PULL_SUBSC_NAME'] if os.environ['PULL_SUBSC_NAME'] else 'pull_scores_sub'
subsc_path = sub.subscription_path(prjid, subsc)


def callback(message):
	message.ack()
	print(json.loads(message.data.decode('utf-8')))


if __name__ == '__main__':
	pull = sub.subscribe(subsc_path, callback=callback)
	try:
		pull.result(timeout=30)
	except:
		print("Cancelling...")
		pull.cancel()
