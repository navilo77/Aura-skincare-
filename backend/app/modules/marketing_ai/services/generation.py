import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations.storage import s3_client
from app.modules.marketing_ai.models import (
    MarketingAILog,
    MarketingAsset,
    MarketingContent,
)
from app.modules.marketing_ai.repositories.marketing import (
    MarketingAILogRepository,
    MarketingAssetRepository,
    MarketingContentRepository,
    MarketingTemplateRepository,
)


class MarketingGenerationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.template_repo = MarketingTemplateRepository(session)
        self.content_repo = MarketingContentRepository(session)
        self.asset_repo = MarketingAssetRepository(session)
        self.log_repo = MarketingAILogRepository(session)

    async def generate_content(
        self,
        template_id: uuid.UUID,
        variables: dict[str, Any],
        campaign_id: uuid.UUID | None = None,
        user_id: uuid.UUID | None = None,
    ) -> MarketingContent:
        template = await self.template_repo.get_by_id(template_id)
        if not template or not template.is_active:
            raise ValueError("Template not found or inactive")

        # Log the generation attempt
        log = MarketingAILog(
            agent="content_generator",
            prompt_version=template.name,
            extra_metadata=json.dumps(
                {"template_id": str(template_id), "variables": variables}
            ),
        )
        await self.log_repo.create(log)

        # Simple template rendering
        prompt = template.prompt
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            prompt = prompt.replace(placeholder, str(value))

        # TODO: Integrate with actual AI provider (OpenAI, Anthropic, etc.)
        # For now, generate mock content
        generated_content = self._mock_generate(prompt, template.content_type)

        # Create content record
        content = MarketingContent(
            campaign_id=campaign_id,
            template_id=template_id,
            content_type=template.content_type,
            title=variables.get("title", f"Generated {template.content_type}"),
            body=generated_content,
            extra_metadata=json.dumps({"variables": variables, "prompt": prompt}),
        )
        created_content = await self.content_repo.create(content)

        # Update log with token usage (mock)
        log.token_usage = len(prompt) // 4 + len(generated_content) // 4
        log.extra_metadata = json.dumps({"content_id": str(created_content.id)})
        await self.session.flush()

        return created_content

    def _mock_generate(self, prompt: str, content_type: str) -> str:
        """Mock content generation - replace with actual AI integration"""
        if content_type == "email":
            return f"Subject: {prompt}\n\nDear Customer,\n\nThis is a generated email based on the prompt: {prompt}\n\nBest regards,\nAura Skincare Team"
        elif content_type == "social_media":
            return f"✨ {prompt} ✨\n\n#AuraSkincare #Beauty #SkincareRoutine"
        elif content_type == "blog":
            return f"# {prompt}\n\nThis is a generated blog post based on the prompt: {prompt}\n\n## Introduction\n\nContent goes here...\n\n## Conclusion\n\nThanks for reading!"
        elif content_type == "ad_copy":
            return f"🎯 {prompt}\n\nLimited time offer! Shop now at Aura Skincare."
        elif content_type == "product_description":
            return f"Product: {prompt}\n\nThis amazing product will transform your skincare routine. Made with premium ingredients for visible results."
        else:
            return f"Generated content for: {prompt}"

    async def generate_from_prompt(
        self,
        prompt: str,
        content_type: str,
        campaign_id: uuid.UUID | None = None,
        user_id: uuid.UUID | None = None,
    ) -> MarketingContent:
        # Log the generation attempt
        log = MarketingAILog(
            agent="content_generator",
            prompt_version="direct_prompt",
            extra_metadata=json.dumps({"prompt": prompt, "content_type": content_type}),
        )
        await self.log_repo.create(log)

        # TODO: Integrate with actual AI provider
        generated_content = self._mock_generate(prompt, content_type)

        content = MarketingContent(
            campaign_id=campaign_id,
            content_type=content_type,
            title=f"AI Generated {content_type}",
            body=generated_content,
            extra_metadata=json.dumps({"prompt": prompt}),
        )
        created_content = await self.content_repo.create(content)

        log.token_usage = len(prompt) // 4 + len(generated_content) // 4
        log.extra_metadata = json.dumps({"content_id": str(created_content.id)})
        await self.session.flush()

        return created_content


class MarketingAssetService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.asset_repo = MarketingAssetRepository(session)

    async def upload_asset(
        self,
        file_content: bytes,
        filename: str,
        content_type: str,
        asset_type: str,
        marketing_content_id: uuid.UUID | None = None,
    ) -> MarketingAsset:
        if s3_client is None:
            raise RuntimeError("Storage provider is disabled")

        # Upload to S3
        key = f"marketing/{asset_type}/{uuid.uuid4()}/{filename}"
        result = s3_client.upload_file(file_content, key, content_type)

        if not result.get("success"):
            raise ValueError(f"Failed to upload asset: {result.get('error')}")

        asset = MarketingAsset(
            content_id=marketing_content_id,
            asset_type=asset_type,
            url=result["url"],
            extra_metadata=json.dumps({"s3_key": key, "original_filename": filename}),
        )
        return await self.asset_repo.create(asset)

    async def upload_generated_image(
        self,
        image_data: bytes,
        marketing_content_id: uuid.UUID | None = None,
    ) -> MarketingAsset:
        return await self.upload_asset(
            file_content=image_data,
            filename="generated_image.png",
            content_type="image/png",
            asset_type="generated_image",
            marketing_content_id=marketing_content_id,
        )


import json
