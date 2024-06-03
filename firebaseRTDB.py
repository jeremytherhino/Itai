import time
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin

# Create a new document in Firestore
def create_document(collection, document_data):

    if not firebase_admin._apps:
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    doc_ref = db.collection(collection).document(str(time.time()).replace(".",""))
    doc_ref.set(document_data)
    print('Document created with ID:', doc_ref.id)

# # Usage example
# create_document('users', {'from': 'b@example.com', 'to': 'a@a.com', 'msg':'bye4'})

# Read a document from Firestore
def read_document(collection, document_id):
    
    if not firebase_admin._apps:
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    doc_ref = db.collection(collection).document(document_id)
    document = doc_ref.get()
    if document.exists:
        print('Document data:', document.to_dict())
    else:
        print('No such document!')

# # Usage example
# read_document('users', '123')

def read_all_documents(collection, from_value, to_value):
    # Initialize the app if it hasn't been already
    if not firebase_admin._apps:
        cred = credentials.Certificate("key.json")
        firebase_admin.initialize_app(cred)
        
    db = firestore.client()
    # Create a query against the collection
    query_ref = db.collection(collection).where('from', '==', from_value).where('to', '==', to_value)
    # Get all documents that match the query
    docs = query_ref.stream()

    documents = []
    for doc in docs:
        documents.append(doc.to_dict())
        
    if documents:
        for document in documents:
            print('Document data:', document)
    else:
        print('No matching documents found!')

# Usage example
# read_all_documents('users', 'a@a.com','b@example.com')