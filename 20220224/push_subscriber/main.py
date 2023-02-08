import base64
import json
import os
from datetime import datetime

from flask import Flask, request
from google.cloud import firestore

app = Flask(__name__)
app.config['TOKEN'] = os.environ['TOKEN']
db = firestore.Client()

@app.route('/pubsub/push/hand_irr', methods=['POST'])
def pubsub_push_hand_irr():
	print('Push request to activate the irrigation')
	if request.args.get('token', '') != app.config['TOKEN']:
		return 'Invalid request', 404
	envelope = json.loads(request.data.decode('utf-8'))
	data = json.loads(base64.b64decode(envelope['message']['data']))
	# docname = datetime.now().strftime('%Y%m%d')
	# db.collection('hand_activated_irrigation').document(docname).set({
	# 	str(datetime.now().timestamp()): data
	# }, merge=True)
	db.collection('hand_irr').document(str(datetime.now().timestamp())).set(data)
	return 'ok', 200


@app.route('/pubsub/push/humidity', methods=['POST'])
def pubsub_push_humidity():
	print('Push update to the measured humidity value')
	if request.args.get('token', '') != app.config['TOKEN']:
		return 'Invalid request', 404
	envelope = json.loads(request.data.decode('utf-8'))
	data = json.loads(base64.b64decode(envelope['message']['data']))
	db.collection('humidity').document(str(datetime.now().timestamp())).set(data)
	return 'ok', 200


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8082, debug=True)
