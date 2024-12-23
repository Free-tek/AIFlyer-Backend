import firebase_admin
from firebase_admin import credentials, firestore, storage
from src.core.config import settings
import base64
import json
from typing import List
import asyncio
def decode_base_64_to_json(base64_string: str):

    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes)
    output_string = string_bytes.decode("ascii")
    output_json = json.loads(output_string)


    return output_json


cred = credentials.Certificate(decode_base_64_to_json(settings.GOOGLE_CONFIG_BASE64))
firebase_admin.initialize_app(cred
    # , { 'storageBucket': settings.STORAGE_BUCKET }
    )

db = firestore.client()

users_data_ref = db.collection("users_data")

# bucket = storage.bucket()


