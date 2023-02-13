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
	data = json.loads(base64.b64decode(envelope['message']['data']))
	league = data['league']
	group = data['group']
	match = data['match']
	score1 = data['score1']
	score2 = data['score2']
	db.collection('scores').document(league).set(
		#{"foo": "bar"})
		{
			group: {
				match: [score1, score2]
			}
		}, merge=True)
	return 'ok', 200


if __name__ == '__main__':
	app.run(host="127.0.0.1", port=8080, debug=True)
