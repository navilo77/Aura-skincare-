import uuid
from typing import Any

from app.modules.ai.repositories.conversation import (
    ConversationRepository,
    MessageRepository,
)


class ConversationMemory:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ) -> None:
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    async def get_conversation(self, customer_id: uuid.UUID) -> dict[str, Any]:
        conversations = await self.conversation_repository.list_by_user(
            customer_id, skip=0, limit=10
        )
        if not conversations:
            return {
                "summary": "",
                "recent_topics": [],
                "previous_recommendations": [],
            }

        all_messages: list[dict[str, Any]] = []
        for conversation in conversations:
            messages = await self.message_repository.list_by_conversation(
                conversation.id, skip=0, limit=50
            )
            for message in messages:
                all_messages.append(
                    {
                        "role": message.role,
                        "content": message.content,
                        "created_at": (
                            message.created_at.isoformat()
                            if message.created_at
                            else None
                        ),
                    }
                )

        all_messages.sort(key=lambda m: m.get("created_at") or "")

        recent_topics = self._extract_topics(all_messages)
        previous_recommendations = self._extract_recommendations(all_messages)
        summary = self._build_summary(all_messages)

        return {
            "summary": summary,
            "recent_topics": recent_topics,
            "previous_recommendations": previous_recommendations,
        }

    def _extract_topics(self, messages: list[dict[str, Any]]) -> list[str]:
        topics: list[str] = []
        keywords = [
            "moisturizer",
            "cream",
            "serum",
            "sunscreen",
            "cleanser",
            "acne",
            "dry",
            "oil",
            "sensitive",
            "brightening",
            "toner",
            "ময়েশ্চারাইজার",
            "ক্রিম",
            "সিরাম",
            "সানস্ক্রিন",
            "ফেসওয়াশ",
        ]
        seen: set[str] = set()
        for message in messages:
            if message.get("role") != "user":
                continue
            content = message.get("content", "").lower()
            for keyword in keywords:
                if keyword in content and keyword not in seen:
                    seen.add(keyword)
                    topics.append(keyword)
        return topics[:10]

    def _extract_recommendations(self, messages: list[dict[str, Any]]) -> list[str]:
        recommendations: list[str] = []
        for message in messages:
            if message.get("role") != "assistant":
                continue
            content = message.get("content", "")
            if "recommend" in content.lower() or "সাজেস্ট" in content:
                recommendations.append(content[:200])
        return recommendations[-5:]

    def _build_summary(self, messages: list[dict[str, Any]]) -> str:
        if not messages:
            return ""
        recent = messages[-6:]
        parts: list[str] = []
        for message in recent:
            role = message.get("role", "")
            content = message.get("content", "")
            if role and content:
                parts.append(f"{role}: {content[:120]}")
        return "\n".join(parts)
