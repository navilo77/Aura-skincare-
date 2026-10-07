from app.config.settings import settings

if settings.enable_s3:
    from app.integrations.storage.s3 import S3Client, s3_client
else:
    from app.integrations.storage.s3 import S3Client

    s3_client = None

__all__ = ["S3Client", "s3_client"]
