import base64
from datetime import datetime
import json
import os

from flask import Flask, request
from google.cloud import firestore

app = Flask(__name__)
app.config['TOKEN'] = os.environ['TOKEN']

db = firestore.Client()


@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
	if request.args.get('token', '') != app.config['TOKEN']:
		return 'Invalid request', 404
	envelope = json.loads(request.data.decode('utf-8'))
	save_to_db(json.loads(base64.b64decode(envelope['message']['data'])))
	return 'ok', 200


def save_to_db(data):
	db.collection('cheaper_car_warnings').document(data['user_to_warn']).set({
		str(datetime.now().timestamp()): {
			'user_cheaper': data['user_cheaper'],
			'car_cheaper': data['car_cheaper'],
			'your_car': data['car_to_warn']
		}
	})


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8080, debug=True)
