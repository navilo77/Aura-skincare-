import json
import os
from typing import Any

from app.config.settings import settings

if settings.enable_s3:
    import boto3
    from botocore.exceptions import ClientError

    class S3Client:
        def __init__(self):
            self.bucket = settings.s3_bucket or os.getenv(
                "S3_BUCKET", "aura-marketing-assets"
            )
            self.region = settings.aws_region or os.getenv("AWS_REGION", "us-east-1")
            self.access_key = settings.aws_access_key_id or os.getenv(
                "AWS_ACCESS_KEY_ID", ""
            )
            self.secret_key = settings.aws_secret_access_key or os.getenv(
                "AWS_SECRET_ACCESS_KEY", ""
            )

            self.client = None
            if self.access_key and self.secret_key:
                self.client = boto3.client(
                    "s3",
                    region_name=self.region,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                )

        def upload_file(
            self,
            file_content: bytes,
            key: str,
            content_type: str = "application/octet-stream",
        ) -> dict[str, Any]:
            if not self.client:
                return {"success": False, "error": "S3 not configured"}

            try:
                self.client.put_object(
                    Bucket=self.bucket,
                    Key=key,
                    Body=file_content,
                    ContentType=content_type,
                )
                url = f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
                return {"success": True, "url": url, "key": key}
            except ClientError as e:
                return {"success": False, "error": str(e)}

        def upload_json(self, data: dict, key: str) -> dict[str, Any]:
            return self.upload_file(
                json.dumps(data, indent=2).encode("utf-8"), key, "application/json"
            )

        def generate_presigned_url(
            self, key: str, expiration: int = 3600
        ) -> dict[str, Any]:
            if not self.client:
                return {"success": False, "error": "S3 not configured"}

            try:
                url = self.client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket, "Key": key},
                    ExpiresIn=expiration,
                )
                return {"success": True, "url": url}
            except ClientError as e:
                return {"success": False, "error": str(e)}

        def delete_file(self, key: str) -> dict[str, Any]:
            if not self.client:
                return {"success": False, "error": "S3 not configured"}

            try:
                self.client.delete_object(Bucket=self.bucket, Key=key)
                return {"success": True}
            except ClientError as e:
                return {"success": False, "error": str(e)}

    s3_client = S3Client()
else:

    class S3Client:
        pass

    s3_client = None
