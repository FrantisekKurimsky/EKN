"""Handle student submissions to Firebase."""
from datetime import datetime
from uuid import uuid4
import re
import streamlit as st
from utils.firebase_client import get_firebase_clients


def safe_slug(value: str) -> str:
    """Sanitize filename."""
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip())
    return cleaned.strip("_")[:80] or "student"


def save_uploaded_files(topic: str, result_title: str, description: str, files):
    """Save uploaded images to Firebase Storage and metadata to Firestore."""
    db, bucket = get_firebase_clients()
    timestamp = datetime.utcnow()
    submission_id = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"
    folder_prefix = f"submissions/{timestamp.strftime('%Y-%m-%d')}"

    uploaded_files = []
    for uploaded_file in files:
        blob_path = f"{folder_prefix}/{uploaded_file.name}"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(
            uploaded_file.getvalue(),
            content_type=uploaded_file.type or "application/octet-stream",
        )

        uploaded_files.append(
            {
                "name": uploaded_file.name,
                "content_type": uploaded_file.type,
                "size_bytes": uploaded_file.size,
                "storage_path": blob_path,
            }
        )

    metadata = {
        "submission_id": submission_id,
        "topic": topic,
        "result_title": result_title,
        "description": description,
        "submitted_at": timestamp.isoformat(timespec="seconds") + "Z",
        "files": uploaded_files,
    }

    db.collection("student_submissions").document(submission_id).set(metadata)
    return metadata
