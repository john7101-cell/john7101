from ..models import ProductBrief, ProductInput
from .base import Agent, to_json


class ProductAnalyst(Agent[ProductBrief]):
    """1. Analista de producto y audiencia."""

    name = "product_analyst"
    role = "Product & audience analyst."
    instructions = """\
Turn the client's product info into a creative brief for UGC writers.
- Explain the product the way a friend would, in plain English.
- Find 2-4 realistic US audience segments and, for each, the concrete daily-life moments where the
  product genuinely helps (time of day, place, what's going wrong right before).
- Separate claims we may say (descriptive facts + the verified claims provided) from claims to avoid.
- Frame the price the way a regular shopper thinks about it ("less than a DoorDash order").
Never invent certifications, studies or numbers that were not provided."""
    output_model = ProductBrief

    def analyze(self, product: ProductInput) -> ProductBrief:
        return self.run(f"Client product info:\n{to_json(product)}")
