from ..models import ComplianceReview, ProductBrief, ProductInput, Script
from .base import Agent, to_json


class ComplianceOfficer(Agent[ComplianceReview]):
    """7. Revisor de cumplimiento (políticas de TikTok Shop US y FTC)."""

    name = "compliance_officer"
    role = "Compliance reviewer for TikTok Shop US content policies and FTC endorsement guidelines."
    instructions = """\
Review the script line by line against the compliance rules.
- blocker = would get the video removed, the shop penalized, or is deceptive (unverified efficacy,
  health/medical claims, fake results timelines, fake urgency, misleading price, impersonation).
- warning = risky wording that should be softened.
- Always list required_disclosures (AIGC label for AI-generated people/voices, #ad / affiliate disclosure,
  plus anything product-specific).
- passed = true only when there are zero blockers."""
    output_model = ComplianceReview

    def review(self, script: Script, product: ProductInput, brief: ProductBrief) -> ComplianceReview:
        return self.run(
            f"Product info (verified_claims are the only allowed efficacy claims):\n{to_json(product)}\n\n"
            f"Safe claims / claims to avoid:\n{to_json({'safe': brief.safe_claims, 'avoid': brief.claims_to_avoid})}\n\n"
            f"Script:\n{to_json(script)}"
        )
