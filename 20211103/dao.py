import json
import random
from datetime import datetime
from uuid import uuid4, UUID
from google.cloud import firestore

import common


class DAO:

    def __init__(self):
        self.db = firestore.Client()
        self.col = self.db.collection('secret_santas')

    def add(self, email, name, extraction_date: datetime, partecipants: list, **kwargs):
        # froms = partecipants.copy()
        # tos = partecipants.copy()
        santas = []

        # for f in froms:
        #     possible_tos = tos.copy()
        #     if f in possible_tos:
        #         possible_tos.remove(f)
        #     i = random.randint(0, len(possible_tos) - 1)
        #     to = possible_tos[i]
        #     tos.remove(to)
        #     santas.append({
        #         'from': f,
        #         'to': to
        #     })

        for f, t in common.secret_santa_pairs(partecipants):
            santas.append({
                'from': f,
                'to': t
            })

        id = str(uuid4())
        self.col.document(id).set({
            'created_by': email,
            'name': name,
            'extraction_date': extraction_date,
            'santas': santas
        })

        return {
            'uuid': id,
            'name': name
        }

    def get(self, santa_id: UUID):
        doc = self.col.document(str(santa_id)).get(['santas'])
        return doc.to_dict()['santas'] if doc.exists else None

    def get_created_by(self, email):
        docs = []
        for doc in self.col.where("created_by", "==", email).stream():
            docs.append(doc.id)
        return docs

    def get_receivers_for(self, name):
        receivers = []
        for doc in self.col.list_documents():
            id = doc.id
            doc = doc.get().to_dict()
            santas = doc['santas']
            for s in santas:
                if s['from'] == name:
                    receivers.append({
                        'list': id,
                        'to': s['to']
                    })
                    break
        return receivers

    def clean(self):
        for d in self.col.list_documents():
            d.delete()


if __name__ == '__main__':
    dao = DAO()
    dao.clean()
    with open('data.json') as f:
        data = json.load(f)
    for k, v in data.items():
        v['extraction_date'] = common.date_from_str(v['extraction-date'], '%Y-%m-%dT%H:%M:%SZ')
        id = dao.add(k, **v)['uuid']
        print(dao.get(UUID(id)))

    print(dao.get_receivers_for("Riccardo Lancellotti"))
