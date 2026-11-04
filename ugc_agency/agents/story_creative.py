from ..models import ConceptBoard, PersonaRoster, ProductBrief, TrendInsights
from .base import Agent, to_json


class StoryCreative(Agent[ConceptBoard]):
    """4. Creativo de historias de la vida cotidiana."""

    name = "story_creative"
    role = "Creative who pitches everyday-life story concepts."
    instructions = """\
Pitch short story concepts where a character narrates a moment of their normal day and the product
appears because it naturally helps in that moment.
- Start from life, not the product: a situation, a small problem or feeling, a tiny resolution.
- Each concept uses one of the recommended formats and one character (by persona_id).
- The product_moment must be specific and unforced (where it is, how they grab it, what they say).
- Vary situations, times of day and emotional tone (funny, tired, relieved, chaotic, cozy).
- Use ids c1, c2, c3..."""
    output_model = ConceptBoard

    def pitch(
        self, brief: ProductBrief, trends: TrendInsights, roster: PersonaRoster, count: int
    ) -> ConceptBoard:
        return self.run(
            f"Pitch exactly {count} concepts, spreading them across the characters.\n\n"
            f"Product brief:\n{to_json(brief)}\n\nFormats & hooks:\n{to_json(trends)}\n\n"
            f"Characters:\n{to_json(roster)}"
        )
