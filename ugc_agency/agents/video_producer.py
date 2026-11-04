from ..models import Persona, ShotList, VideoProductionPack
from .base import Agent, to_json


class VideoProducer(Agent[VideoProductionPack]):
    """9. Productor de video IA: prompts listos para generadores de video y voz."""

    name = "video_producer"
    role = "AI video producer who writes prompts for text/image-to-video models and voice generation."
    instructions = """\
Convert the shot list into a production pack for AI video tools (Veo, Kling, Sora, Runway, Hailuo, etc.).
- character_reference_prompt: one detailed prompt to generate a consistent reference image of the
  character (same face/outfit across scenes): natural skin texture, everyday clothes, realistic phone
  photo, no beauty filter. Must not resemble any real person.
- One scene prompt per shot: subject + action + setting + "shot on iPhone front camera, vertical 9:16,
  natural handheld shake, available light, unedited UGC look", plus duration.
- negative_prompt per scene: studio lighting, cinematic, perfect skin, plastic look, text artifacts,
  extra fingers, warped product label, logo distortion.
- voice: describe a natural voice matching the character (age, accent/region, energy) for TTS, with
  low-ish stability for natural variation.
- caption_style and post_production_steps (assemble, add TikTok auto-captions, add AIGC label, etc.)."""
    output_model = VideoProductionPack

    def produce(self, shot_list: ShotList, persona: Persona, product_name: str) -> VideoProductionPack:
        return self.run(
            f"Product (keep the real packaging visible and undistorted): {product_name}\n\n"
            f"Character:\n{to_json(persona)}\n\nShot list:\n{to_json(shot_list)}"
        )
