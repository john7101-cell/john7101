from ..models import Persona, ProductBrief, Script, StoryConcept
from .base import Agent, to_json


class Scriptwriter(Agent[Script]):
    """5. Guionista de UGC."""

    name = "scriptwriter"
    role = "UGC scriptwriter who writes exactly how real people talk on TikTok."
    instructions = """\
Write a 20-45 second vertical video script for the concept, in the character's own voice.
- The first beat (0-2s) is the hook: an in-the-moment line or action, not a product intro.
- Spoken lines read like a transcript of someone talking to their phone: contractions, filler,
  self-corrections, specific details from their life, use the character's verbal habits.
- The product appears in the middle of the story; show it being used, don't list features.
- Use only safe claims from the brief. Sensory, personal observations are fine.
- End with a soft, in-character CTA (TikTok Shop orange cart / "I'll link it").
- full_voiceover = every spoken line in order, nothing else (it goes straight to text-to-speech).
- If revision notes are provided, address every one of them."""
    output_model = Script

    def write(
        self,
        concept: StoryConcept,
        persona: Persona,
        brief: ProductBrief,
        revision_notes: list[str] | None = None,
        previous: Script | None = None,
    ) -> Script:
        prompt = (
            f"Concept:\n{to_json(concept)}\n\nCharacter:\n{to_json(persona)}\n\n"
            f"Product brief:\n{to_json(brief)}"
        )
        if previous and revision_notes:
            notes = "\n".join(f"- {n}" for n in revision_notes)
            prompt += f"\n\nPrevious draft:\n{to_json(previous)}\n\nRevision notes to address:\n{notes}"
        return self.run(prompt)
