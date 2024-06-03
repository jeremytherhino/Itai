import time
import uuid

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



class FirestoreManager:
    def __init__(self):
        # Initialize Firebase Admin with the provided credentials file
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def add_data(self, collection_name, document_id, data):
        # Add a new document with the provided data to the specified collection
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc_ref.set(data)
        print(f"Document '{document_id}' added to collection '{collection_name}'")

    def get_data(self, collection_name, document_id):
        # Retrieve data from the specified document in the collection
        doc_ref = self.db.collection(collection_name).document(document_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Document '{document_id}' not found in collection '{collection_name}'")
            return None



    def get_all_data(self, collection_name):
        print("db", self.db.collection(collection_name))
        print(f"Fetching data from collection: {collection_name}")
        docs = self.db.collection(collection_name).stream()
        data = {doc.id: doc.to_dict() for doc in docs}
        print(f"Fetched data: {data}")
        return data
    def add_data2(self, collection_name, document_id, sub_collection_name, data):

        doc_ref = self.db.collection(collection_name).document(document_id)
        sub_collection_ref = doc_ref.collection(sub_collection_name)

        # Add each key-value pair as a document in the sub-collection
        for key, value in data.items():
            sub_collection_ref.document(key).set({"value": value})

    def add_data3(self, collection_name, sender_mail, receiver_mail, data):

        id = str(time.time()).replace(".","")
        doc_ref = self.db.collection("chats").document(id)
        sub_collection_ref = doc_ref.collection(id)
        # doc_ref = self.db.collection("chats").document(sender_mail)
        # sub_collection_ref = doc_ref.collection(receiver_mail)
        # sub_doc_ref = sub_collection_ref.document(str(uuid.uuid4()))
        # sub_sub_collection_ref = sub_doc_ref.collection('messages')

        # Add each key-value pair as a document in the sub-collection
        for key, value in data.items():
            sub_collection_ref.document(key).set({"value": value})



# # Example usage
# if __name__ == "__main__":
#     client = FirestoreManager()
#     collection_name = "A"
#     document_id = "example_doc"
#     sub_collection_name = "B"
#     data = {
#         "key1": "value1",
#         "key2": "value2",
#         "key3": "value3"
#     }
#
#     client.add_data2(collection_name, document_id, sub_collection_name, data)