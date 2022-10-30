import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

firebaseConfig = {
    "apiKey": "AIzaSyBS3rDg9hVYqnj5A-_aXb5ttu-6rxJVKTc",
    "authDomain": "mkscoding-32b2c.firebaseapp.com",
    "databaseURL": "https://mkscoding-32b2c-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "mkscoding-32b2c",
    "storageBucket": "mkscoding-32b2c.appspot.com",
    "messagingSenderId": "583816681550",
    "appId": "1:583816681550:web:9be9e1956d9ae6700b4b1f"
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN
