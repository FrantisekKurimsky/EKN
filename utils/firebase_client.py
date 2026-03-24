"""Firebase authentication and client management."""
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, storage as firebase_storage


@st.cache_resource
def get_firebase_clients():
    """Initialize and return Firebase Firestore and Storage clients."""
    if "firebase" not in st.secrets:
        raise RuntimeError("Firebase nie je nakonfigurovany v .streamlit/secrets.toml.")

    firebase_config = st.secrets["firebase"]
    if "service_account" not in firebase_config:
        raise RuntimeError("Chyba sekcia [firebase.service_account] v secrets.")
    if "storage_bucket" not in firebase_config:
        raise RuntimeError("Chyba firebase.storage_bucket v secrets.")

    service_account_info = dict(firebase_config["service_account"])
    required_fields = [
        "type",
        "project_id",
        "private_key_id",
        "private_key",
        "client_email",
        "client_id",
        "token_uri",
    ]
    missing_fields = [field for field in required_fields if not service_account_info.get(field)]
    if missing_fields:
        raise RuntimeError(f"V secrets chybaju povinne Firebase polia: {', '.join(missing_fields)}")

    placeholder_markers = ["PASTE_FROM_SERVICE_ACCOUNT_JSON", "PASTE_KEY_HERE", "..."]
    for key, value in service_account_info.items():
        if isinstance(value, str) and any(marker in value for marker in placeholder_markers):
            raise RuntimeError(
                f"Pole firebase.service_account.{key} stale obsahuje placeholder hodnotu."
            )

    if "private_key" in service_account_info:
        service_account_info["private_key"] = service_account_info["private_key"].replace("\\n", "\n")

    bucket_name = str(firebase_config["storage_bucket"]).strip()
    if bucket_name.startswith("gs://"):
        bucket_name = bucket_name[len("gs://"):]
    bucket_name = bucket_name.rstrip("/")
    if not bucket_name:
        raise RuntimeError("firebase.storage_bucket je prázdny.")

    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_info)
        firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})

    db = firestore.client()
    bucket = firebase_storage.bucket()
    return db, bucket
