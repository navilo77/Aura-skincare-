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

    def build_context(self, user_message: str, history: list[dict[str, Any]]) -> str:
        prompt_parts = []
        if history:
            prompt_parts.append("\n\nHistory:")
            for entry in history[-10:]:
                role = entry.get("role", "user")
                content = entry.get("content", "")
                prompt_parts.append(f"{role}: {content}")
        prompt_parts.append(f"\n\nUser: {user_message}\nAssistant:")
        return "\n".join(prompt_parts)
