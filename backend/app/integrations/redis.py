from typing import Any, cast

from app.config.settings import settings

try:
    from redis.asyncio import Redis
except ImportError:  # pragma: no cover
    Redis = None  # type: ignore[misc, assignment]


class RedisClient:
    """
    Single Source of Truth for all Redis operations.

    This class is the ONLY layer allowed to communicate directly with
    `redis.asyncio.Redis`. Business modules must never import
    `redis.asyncio.Redis` and must use `redis_client` wrapper methods only.

    Purpose:
        Centralize Redis connection management and provide a stable,
        encapsulated interface for cache, session, queue, and pub/sub
        operations across the application.

    Architecture Rule:
        All Redis access flows through RedisClient. Implementation details
        remain fully encapsulated so business modules stay decoupled from
        the Redis driver. This abstraction allows future migration to
        another Redis-compatible backend (for example, Valkey, DragonflyDB,
        or Upstash) without changing any business module.

    Responsibilities:
        - Manage Redis connection lifecycle (connect, disconnect, ping)
        - Expose typed async wrapper methods for Redis commands
        - Preserve configuration, timeouts, and error-handling policies
        - Shield business modules from Redis driver changes

    Do:
        - Inject or import the shared `redis_client` instance
        - Call wrapper methods such as `get`, `set`, `delete`, `rpush`
        - Add new wrapper methods here when new Redis operations are needed

    Do Not:
        - Import or instantiate `redis.asyncio.Redis` outside this class
        - Access `_client` or driver internals from business modules
        - Bypass RedisClient to execute raw Redis commands
        - Embed Redis connection logic in routes, services, or repositories
    """

    def __init__(self, url: str = "") -> None:
        self._url = url or settings.redis_url
        self._client: Any = None

    async def connect(self) -> None:
        if Redis is None:
            raise RuntimeError("redis package is not installed")
        if self._client is None:
            self._client = Redis.from_url(
                self._url,
                socket_connect_timeout=5,
                socket_timeout=5,
            )

    async def disconnect(self) -> None:
        if self._client is not None:
            try:
                await self._client.aclose()
            except Exception:
                pass
            self._client = None

    @property
    def client(self) -> Any:
        if self._client is None:
            raise RuntimeError("RedisClient is not connected")
        return self._client

    async def get(self, key: str) -> bytes | None:
        return cast("bytes | None", await self.client.get(key))

    async def set(self, key: str, value: str, ex: int | None = None) -> bool:
        return cast("bool", await self.client.set(key, value, ex=ex))

    async def delete(self, key: str) -> int:
        return cast("int", await self.client.delete(key))

    async def exists(self, key: str) -> int:
        return cast("int", await self.client.exists(key))

    async def rpush(self, key: str, *values: str) -> int:
        return cast("int", await self.client.rpush(key, *values))

    async def lrange(self, key: str, start: int, end: int) -> list[bytes]:
        return cast("list[bytes]", await self.client.lrange(key, start, end))

    async def ltrim(self, key: str, start: int, end: int) -> None:
        await self.client.ltrim(key, start, end)

    async def hset(self, key: str, mapping: dict[str, Any]) -> int:
        return cast("int", await self.client.hset(key, mapping=mapping))

    async def hgetall(self, key: str) -> dict[bytes, bytes]:
        return cast("dict[bytes, bytes]", await self.client.hgetall(key))

    async def expire(self, key: str, ttl: int) -> bool:
        return cast("bool", await self.client.expire(key, ttl))

    async def ping(self) -> bool:
        try:
            await self.client.ping()
            return True
        except Exception:
            return False


redis_client = RedisClient()
