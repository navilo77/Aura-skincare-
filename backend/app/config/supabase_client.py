"""
Supabase Client Configuration

This module initializes the Supabase client for both auth and storage operations.
It provides two clients:
- supabase: Regular client for public operations (frontend-safe)
- supabase_admin: Admin client for server-side operations (service role)
"""

from functools import lru_cache

from app.config.settings import settings


@lru_cache
def get_supabase_client() -> object:
    """
    Get a Supabase client configured with the anon key.

    This client should only be used for user-facing operations.
    Never expose the service role key to the frontend.

    Returns:
        Supabase client instance
    """
    try:
        from supabase import Client, create_client

        client = create_client(settings.supabase_url, settings.supabase_anon_key)
        return client
    except ImportError:
        raise ImportError(
            "supabase-py is required. Install with: pip install supabase-py"
        )


@lru_cache
def get_supabase_admin_client() -> object:
    """
    Get a Supabase client configured with the service role key.

    This client has elevated privileges and should ONLY be used in
    server-side code. Never expose this client to the frontend.

    Returns:
        Supabase client instance with admin privileges
    """
    try:
        from supabase import Client, create_client

        client = create_client(
            settings.supabase_url, settings.supabase_service_role_key
        )
        return client
    except ImportError:
        raise ImportError(
            "supabase-py is required. Install with: pip install supabase-py"
        )


# Convenience instances for direct import
# Note: These are cached, so they're safe to import multiple times
supabase: object = get_supabase_client()
supabase_admin: object = get_supabase_admin_client()


class SupabaseStorageManager:
    """
    Manages Supabase Storage operations for file uploads and downloads.
    """

    def __init__(self):
        self._client = get_supabase_client()
        self._admin_client = get_supabase_admin_client()

    async def create_bucket(
        self,
        bucket_name: str,
        public: bool = False,
        file_size_limit: int = 50 * 1024 * 1024,  # 50MB by default
    ) -> bool:
        """
        Create a new storage bucket.

        Args:
            bucket_name: Name of the bucket to create
            public: Whether the bucket is publicly accessible
            file_size_limit: Maximum file size in bytes

        Returns:
            True if bucket was created successfully
        """
        try:
            response = await self._admin_client.storage.create_bucket(
                bucket_name,
                {
                    "public": public,
                    "file_size_limit": file_size_limit,
                    "allowed_file_types": [
                        "image/jpeg",
                        "image/png",
                        "image/webp",
                        "image/avif",
                        "application/pdf",
                    ],
                },
            )
            return True
        except Exception as e:
            # Bucket might already exist
            raise RuntimeError(f"Failed to create bucket {bucket_name}: {e}")

    async def upload_file(
        self,
        bucket_name: str,
        file_path: str,
        file_content: bytes,
        cache_control: str = "max-age=3600",
        content_type: str = "image/jpeg",
    ) -> str:
        """
        Upload a file to storage.

        Args:
            bucket_name: Name of the bucket
            file_path: Path within the bucket (e.g., "products/123.jpg")
            file_content: Raw file bytes
            cache_control: Cache control header
            content_type: MIME type of the file

        Returns:
            Public URL of the uploaded file
        """
        try:
            response = self._client.storage.from_(bucket_name).upload(
                path=file_path,
                file=file_content,
                options={"cacheControl": cache_control, "contentType": content_type},
            )
            return response
        except Exception as e:
            raise RuntimeError(
                f"Failed to upload file to {bucket_name}/{file_path}: {e}"
            )

    async def get_public_url(self, bucket_name: str, file_path: str) -> str:
        """
        Get the public URL for a file.

        Args:
            bucket_name: Name of the bucket
            file_path: Path within the bucket

        Returns:
            Public URL string
        """
        return self._client.storage.from_(bucket_name).get_public_url(file_path)

    async def get_signed_url(
        self, bucket_name: str, file_path: str, expires_in: int = 3600
    ) -> str:
        """
        Get a signed URL for a file.

        Args:
            bucket_name: Name of the bucket
            file_path: Path within the bucket
            expires_in: Expiration time in seconds

        Returns:
            Signed URL string
        """
        try:
            response = self._client.storage.from_(bucket_name).create_signed_url(
                file_path, expires_in
            )
            return response["signedURL"]
        except Exception as e:
            raise RuntimeError(f"Failed to create signed URL: {e}")

    async def delete_file(self, bucket_name: str, file_path: str) -> bool:
        """
        Delete a file from storage.

        Args:
            bucket_name: Name of the bucket
            file_path: Path within the bucket

        Returns:
            True if deleted successfully
        """
        try:
            response = self._client.storage.from_(bucket_name).remove([file_path])
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to delete file {file_path}: {e}")

    async def list_files(self, bucket_name: str, prefix: str = "") -> list:
        """
        List files in a bucket.

        Args:
            bucket_name: Name of the bucket
            prefix: Optional prefix to filter files

        Returns:
            List of file information
        """
        try:
            response = self._client.storage.from_(bucket_name).list(prefix)
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to list files in {bucket_name}: {e}")


# Initialize storage manager
storage_manager = SupabaseStorageManager()
