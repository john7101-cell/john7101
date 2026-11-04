from ..models import ComplianceReview, Persona, PostPackage, Script
from .base import Agent, to_json


class SocialCopywriter(Agent[PostPackage]):
    """10. Copywriter social: caption, hashtags y comentario fijado."""

    name = "social_copywriter"
    role = "Writes TikTok captions that sound like the character, not a brand."
    instructions = """\
Write the post copy in the character's voice.
- caption: short, lowercase-friendly, conversational, max ~150 characters before hashtags.
- 3-6 hashtags: mix niche/community tags with #tiktokshop-style discovery tags; no hashtag stuffing.
- pinned_comment: something the character would pin (answering a likely question, casual).
- disclosure_text: the paid/affiliate disclosure that must appear (e.g. "#ad" or "I earn commission").
  Remind that the AI-generated content label must be switched on when posting.
- best_posting_window_et: a reasonable window in US Eastern time for this audience."""
    output_model = PostPackage

    def write(self, script: Script, persona: Persona, compliance: ComplianceReview) -> PostPackage:
        return self.run(
            f"Character:\n{to_json(persona)}\n\nScript:\n{to_json(script)}\n\n"
            f"Required disclosures:\n{to_json(compliance.required_disclosures)}"
        )
