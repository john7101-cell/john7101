from ..models import Persona, Script, ShotList
from .base import Agent, to_json


class SceneDirector(Agent[ShotList]):
    """8. Director de escena: shot list con estética de celular."""

    name = "scene_director"
    role = "Director who plans phone-shot, vertical UGC scenes."
    instructions = """\
Break the approved script into a 9:16 shot list that looks self-filmed on an iPhone.
- Camera: selfie at arm's length, phone propped on the dashboard/counter, quick handheld B-roll of the
  product in use, occasional jump cuts. No drones, dollies, studio lights or cinematic grading.
- Locations and light come from the character's real life (car at golden hour, kitchen with overhead
  light, bathroom mirror, break room fluorescents).
- Include natural audio (traffic, kids, TV in the background, dishwasher).
- Each shot carries its spoken_line so editors can sync voice.
- editing_notes: native TikTok text overlays, auto-captions, jump cuts, no fancy transitions."""
    output_model = ShotList

    def plan(self, script: Script, persona: Persona) -> ShotList:
        return self.run(f"Character:\n{to_json(persona)}\n\nApproved script:\n{to_json(script)}")
