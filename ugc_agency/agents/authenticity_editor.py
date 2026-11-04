from ..models import AuthenticityReview, Persona, Script
from .base import Agent, to_json


class AuthenticityEditor(Agent[AuthenticityReview]):
    """6. Editor de autenticidad: ¿esto parece un anuncio o una persona real?"""

    name = "authenticity_editor"
    role = "Ruthless authenticity editor. You've watched 10,000 TikToks and can smell an ad instantly."
    instructions = """\
Score how natural the script feels from 1 (obvious ad) to 10 (indistinguishable from a real person's post).
- Flag every line that sounds scripted, salesy, too polished, too perfect, or off-character.
- Check the hook works without the product, the story is a real daily-life moment, and the CTA is soft.
- Note what already feels real so the writer keeps it.
- rewrite_notes must be concrete ("replace line 3 with something she'd say while parking, e.g. ...").
- verdict = "approve" only if score >= the threshold given and there are no ad-speak flags left."""
    output_model = AuthenticityReview

    def review(self, script: Script, persona: Persona, threshold: int) -> AuthenticityReview:
        return self.run(
            f"Approval threshold: {threshold}/10\n\nCharacter:\n{to_json(persona)}\n\nScript:\n{to_json(script)}"
        )
