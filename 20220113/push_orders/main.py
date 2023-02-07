import base64
import json
import os
from datetime import datetime

from flask import Flask, request
from google.cloud import firestore

app = Flask(__name__)
app.config['TOKEN'] = os.environ['TOKEN']
db = firestore.Client()


@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
	print('Received pubsub push')
	if request.args.get('token', '') != app.config['TOKEN']:
		return 'Invalid request', 404
	envelope = json.loads(request.data.decode('utf-8'))
	data = json.loads(base64.b64decode(envelope['message']['data']))
	print(data)
	db.collection('wine_orders').document(str(datetime.now())).set(data)
	return 'OK', 200


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8080, debug=True)
