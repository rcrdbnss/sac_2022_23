from google.cloud import pubsub_v1

sub = pubsub_v1.SubscriberClient()
subsc_path = sub.subscription_path('rbenassi-20220413', 'cheaper_cars_pull_sub')


def callback(message):
	message.ack()
	print(message.data.decode('utf-8'))


if __name__ == '__main__':
	pull = sub.subscribe(subsc_path, callback=callback)
	try:
		pull.result(timeout=30)
	except:
		pull.cancel()
