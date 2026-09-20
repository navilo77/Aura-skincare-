from pathlib import Path
from typing import Any


class PromptManager:
    def __init__(self) -> None:
        self.prompts: dict[str, str] = {}
        prompts_dir = Path(__file__).parent.parent / "prompts"
        for prompt_file in prompts_dir.glob("*.md"):
            name = prompt_file.stem
            self.prompts[name] = prompt_file.read_text(encoding="utf-8")

    def get(self, name: str) -> str | None:
        return self.prompts.get(name)

    def get_system_prompt(self) -> str:
        return self.prompts.get("system", "")

    def get_router_prompt(self) -> str:
        return self.prompts.get("router", "")

    def get_customer_prompt(self) -> str:
        return self.prompts.get("customer", "")

    def get_guardrails(self) -> str:
        return self.prompts.get("guardrails", "")

    def build_context(self, user_message: str, history: list[dict[str, Any]]) -> str:
        prompt_parts = [self.get_system_prompt(), self.get_guardrails()]
        if history:
            prompt_parts.append("\n\nConversation history:")
            for entry in history[-10:]:
                role = entry.get("role", "user")
                content = entry.get("content", "")
                prompt_parts.append(f"{role}: {content}")
        prompt_parts.append(f"\n\nUser: {user_message}\nAssistant:")
        return "\n".join(prompt_parts)
