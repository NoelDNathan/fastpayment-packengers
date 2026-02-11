"""Object storage service for MinIO/S3-compatible backends."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import BinaryIO
from urllib.parse import urlparse

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.config import settings
import re



class ObjectStorageService:
    """Handle upload and cleanup operations in object storage."""

    def __init__(self) -> None:
        scheme = "https" if settings.minio_secure else "http"
        endpoint = settings.minio_endpoint.strip()
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            endpoint_url = endpoint
        else:
            endpoint_url = f"{scheme}://{endpoint}"

        self._bucket_name = settings.minio_bucket_name

        self._client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
            config=Config(signature_version="s3v4"),
            region_name=settings.minio_region,
        )

    async def ensure_bucket_exists(self) -> None:
        """Create the configured bucket if it does not exist."""
        await asyncio.to_thread(self._ensure_bucket_exists_sync)

    async def upload_invoice(
        self,
        file_obj: BinaryIO,
        *,
        object_key: str,
        content_type: str,
    ) -> str:
        """Upload invoice file and return the object URL."""
        await asyncio.to_thread(
            self._client.upload_fileobj,
            file_obj,
            self._bucket_name,
            object_key,
            ExtraArgs={"ContentType": content_type},
        )
        return f"s3://{self._bucket_name}/{object_key}"

    async def delete_object(self, object_key: str) -> None:
        """Delete an object from storage."""
        await asyncio.to_thread(
            self._client.delete_object,
            Bucket=self._bucket_name,
            Key=object_key,
        )

    async def generate_download_url(
        self, invoice_file_url: str, expires_in_seconds: int = 900
    ) -> str:
        """Generate a temporary download URL for a stored invoice."""
        object_key = self.extract_object_key(invoice_file_url)
        return await asyncio.to_thread(
            self._client.generate_presigned_url,
            "get_object",
            Params={"Bucket": self._bucket_name, "Key": object_key},
            ExpiresIn=expires_in_seconds,
        )

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Return a safe filename for object keys."""
        clean_name = Path(filename).name.strip().replace(" ", "_")
        clean_name = re.sub(r"[^A-Za-z0-9._-]", "", clean_name)
        return clean_name or "invoice.pdf"

    def extract_object_key(self, invoice_file_url: str) -> str:
        """Extract object key from an s3://bucket/key style URL."""
        parsed_url = urlparse(invoice_file_url)
        if parsed_url.scheme != "s3":
            raise ValueError("Invoice file URL must start with s3://")
        if parsed_url.netloc != self._bucket_name:
            raise ValueError("Invoice file URL bucket does not match configured bucket")

        object_key = parsed_url.path.lstrip("/")
        if not object_key:
            raise ValueError("Invoice file URL does not contain an object key")
        return object_key

    def _ensure_bucket_exists_sync(self) -> None:
        """Sync implementation for bucket existence check."""
        try:
            self._client.head_bucket(Bucket=self._bucket_name)
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")
            if error_code in {"404", "NoSuchBucket", "NotFound"}:
                if settings.minio_region and settings.minio_region != "us-east-1":
                    self._client.create_bucket(
                        Bucket=self._bucket_name,
                        CreateBucketConfiguration={
                            "LocationConstraint": settings.minio_region
                        },
                    )
                else:
                    self._client.create_bucket(Bucket=self._bucket_name)
                return
            raise
