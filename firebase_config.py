import os
import base64
import json
from firebase_admin import credentials, initialize_app, firestore
from dotenv import load_dotenv

load_dotenv()

encoded_key = os.getenv('FIREBASE_SERVICE_KEY')
decoded_key = base64.b64decode(encoded_key)

service_account_info = json.loads(decoded_key)

cred = credentials.Certificate(service_account_info)
initialize_app(cred)

db = firestore.client()
