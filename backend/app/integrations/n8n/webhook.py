from typing import Any

import httpx


class N8NClient:
    def __init__(self, base_url: str = "", timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout

    async def trigger_webhook(
        self, url: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                }
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP {e.response.status_code}",
                "status_code": e.response.status_code,
            }
        except httpx.RequestError as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def trigger_workflow(
        self, workflow_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        url = f"{self.base_url}/webhook/{workflow_id}"
        return await self.trigger_webhook(url, payload)


# Default client - will be configured from settings
n8n_client = N8NClient()
