from ..models import ProductBrief, TrendInsights
from .base import Agent, to_json


class TrendStrategist(Agent[TrendInsights]):
    """2. Estratega de formatos y tendencias de TikTok."""

    name = "trend_strategist"
    role = "TikTok-native format and hook strategist for TikTok Shop US."
    instructions = """\
Recommend evergreen, native TikTok formats that fit this product and feel like real people posting:
e.g. "get ready with me", "day in my life", "come with me to...", "car talk", "things I do after a
12-hour shift", "my 6am routine", "storytime while I cook", "reset with me", "POV" skits, "honest
reaction / first try", "what's in my bag", "small things that make my week easier".
For each format explain why it feels native and give an example hook written as a real person would say it.
Give hook patterns that stop the scroll in the first 1-2 seconds without clickbait, pacing guidance
for 20-45s videos, the audio vibe, and the clichés to avoid. Do not claim specific trending sounds
or current viral data — keep it evergreen."""
    output_model = TrendInsights

    def research(self, brief: ProductBrief) -> TrendInsights:
        return self.run(f"Product brief:\n{to_json(brief)}")
