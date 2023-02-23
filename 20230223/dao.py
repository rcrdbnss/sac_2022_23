import json
import os
import uuid
from datetime import datetime
import common

from google.api_core.exceptions import AlreadyExists
from google.cloud import firestore
from google.cloud import pubsub_v1

pub = pubsub_v1.PublisherClient()

prjid = os.environ['PROJECT_ID'] if os.environ['PROJECT_ID'] else 'rbenassi-20230223'
prjpath = f'projects/{prjid}'


def get_topic_path(hashtag: str):
    topic_path = pub.topic_path(prjid, hashtag)
    # if hashtag not in pub.list_topics(request={"project": prjpath}):
    try:
        pub.create_topic(request={"name": topic_path})
    except AlreadyExists:
        pass
    return topic_path


class DAO:

    def __init__(self):
        self.db = firestore.Client()
        self.messages = self.db.collection('messages')
        self.hashtags = self.db.collection('hashtags')

    def add_message(self, message) -> uuid.UUID:
        id = uuid.uuid4()
        str_id = str(id)
        # global next_id
        # id = f'{next_id}'
        # next_id += 1

        hashtags = common.get_hashtags(message)
        for i in range(0, len(hashtags)):
            hashtags[i] = hashtags[i].replace('#', '').lower()
        timestamp = datetime.now()
        self.messages.document(str_id).set({
            'timestamp': timestamp,
            'message': message,
            'hashtags': hashtags
        })
        for h in hashtags:
            self.hashtags.document(h).set({
                str_id: timestamp
            }, merge=True)
            pub.publish(get_topic_path(h), json.dumps(message).encode('utf-8'))
        return id

    def get_message(self, id: uuid.UUID):
        str_id = str(id)
        doc = self.messages.document(str_id).get()
        if doc.exists:
            doc = doc.to_dict()
            doc['id'] = str_id
            del doc['hashtags']
            return doc
        else:
            return None

    def get_messages_with(self, hashtag: str):
        hashtag = hashtag.replace("#", "").lower()
        doc = self.hashtags.document(hashtag).get()
        msgs = None
        if doc.exists:
            msgs = [k for k in doc.to_dict().keys()]
        return msgs

    def clean(self):
        for d in self.messages.list_documents():
            d.delete()
        for d in self.hashtags.list_documents():
            d.delete()


if __name__ == '__main__':
    dao = DAO()
    dao.clean()
    with open('data.json') as f:
        data = json.load(f)
    for v in data:
        id = dao.add_message(v)
        print(dao.get_message(id))
    print(dao.get_messages_with("ElonMusk"))
    print(dao.get_messages_with("RiccardoBenassi"))
