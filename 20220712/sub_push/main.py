import base64
from flask import Flask, request
from google.cloud import firestore
import json
import os

app = Flask(__name__)
app.config['TOKEN'] = os.environ['TOKEN']
db = firestore.Client()


@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
	print('Received pubsub push')
	if request.args.get('token', '') != app.config['TOKEN']:
		return 'Invalid request', 404
	envelope = json.loads(request.data.decode('utf-8'))
	save_to_db(json.loads(base64.b64decode(envelope['message']['data'])))
	return 'ok', 200


def save_to_db(data):
	user = data['user']
	date = data['date']
	time = data['time']
	db.collection('bracelet_reqs').document(user).set(
		{
			'date': date,
			'time': time
		}, merge=True)


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8080, debug=True)
