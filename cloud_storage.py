import os
from typing import BinaryIO
from google.cloud import storage


storage_client = storage.Client()
bucket_name = os.environ["GCP_STORAGE_BACKEND"]
bucket = storage_client.bucket(bucket_name)


def upload_blob(stream: BinaryIO, filename: str) -> str:
    """
    Upload a file stream to bucket/filename
    """

    blob = bucket.blob(filename, chunk_size=1024 * 1024)
    blob.upload_from_file(stream)

    return f"gc://{bucket_name}/{filename}"


def delete_blob(filepath: str) -> None:
    """
    Delete a file stream from bucket
    """

    blob = bucket.blob(filepath)
    blob.delete()
