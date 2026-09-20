from typing import Any


class BaseMarketingTool:
    name: str = ""
    description: str = ""

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class GenerateProductCaptionTool(BaseMarketingTool):
    name = "generate_product_caption"
    description = "Generate a product caption"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Product caption"}


class GenerateFacebookPostTool(BaseMarketingTool):
    name = "generate_facebook_post"
    description = "Generate a Facebook post"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Facebook post"}


class GenerateInstagramCaptionTool(BaseMarketingTool):
    name = "generate_instagram_caption"
    description = "Generate an Instagram caption"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Instagram caption"}


class GenerateTikTokCaptionTool(BaseMarketingTool):
    name = "generate_tiktok_caption"
    description = "Generate a TikTok caption"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "TikTok caption"}


class GenerateBlogTool(BaseMarketingTool):
    name = "generate_blog"
    description = "Generate a blog post"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Blog post"}


class GenerateEmailTool(BaseMarketingTool):
    name = "generate_email"
    description = "Generate an email"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Email"}


class GenerateCampaignTool(BaseMarketingTool):
    name = "generate_campaign"
    description = "Generate a campaign"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Campaign"}


class GeneratePromotionTool(BaseMarketingTool):
    name = "generate_promotion"
    description = "Generate a promotion"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Promotion"}


class GenerateHashtagsTool(BaseMarketingTool):
    name = "generate_hashtags"
    description = "Generate hashtags"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Hashtags"}


class GenerateProductDescriptionTool(BaseMarketingTool):
    name = "generate_product_description"
    description = "Generate a product description"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Product description"}


class GenerateSEOTitleTool(BaseMarketingTool):
    name = "generate_seo_title"
    description = "Generate an SEO title"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "SEO title"}


class GenerateSEOMetaTool(BaseMarketingTool):
    name = "generate_seo_meta"
    description = "Generate SEO meta description"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "SEO meta"}


class GenerateKeywordsTool(BaseMarketingTool):
    name = "generate_keywords"
    description = "Generate keywords"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Keywords"}


class GenerateCallToActionTool(BaseMarketingTool):
    name = "generate_call_to_action"
    description = "Generate a call to action"

    async def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        return {"tool": self.name, "result": "Call to action"}
