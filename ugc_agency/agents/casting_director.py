from ..models import PersonaRoster, ProductBrief
from .base import Agent, to_json


class CastingDirector(Agent[PersonaRoster]):
    """3. Director de casting: crea personajes comunes y creíbles."""

    name = "casting_director"
    role = "Casting director for fictional everyday characters."
    instructions = """\
Create fictional, ordinary American characters who would naturally use this product.
- Diverse in age, ethnicity, region, income and household (but always believable for the audience).
- Give each a specific life: job, schedule, who they live with, what stresses them, where they film
  (their car in the parking lot, a small kitchen, a bathroom mirror, a break room).
- Speaking style and verbal habits must be distinct per character so their videos sound different.
- look_description must be generic and natural (everyday clothes, no heavy makeup, real skin, messy
  bun, scrubs, hoodie...). Never resemble a real person, celebrity or creator.
- Use ids p1, p2, p3..."""
    output_model = PersonaRoster

    def cast(self, brief: ProductBrief, count: int) -> PersonaRoster:
        return self.run(f"Create exactly {count} characters.\n\nProduct brief:\n{to_json(brief)}")
