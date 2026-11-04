"""Clase base de los agentes de la agencia."""

from __future__ import annotations

import json
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

from ..guidelines import ALL_RULES
from ..llm import LLM

T = TypeVar("T", bound=BaseModel)


def to_json(obj: Any) -> str:
    """Serializa modelos (o listas/dicts de modelos) para incluirlos en un prompt."""
    if isinstance(obj, BaseModel):
        return obj.model_dump_json(indent=2)
    if isinstance(obj, (list, tuple)):
        return json.dumps([json.loads(to_json(o)) for o in obj], indent=2, ensure_ascii=False)
    return json.dumps(obj, indent=2, ensure_ascii=False, default=str)


class Agent(Generic[T]):
    """Un especialista de la agencia: un rol, unas instrucciones y un formato de entrega."""

    name: str = "agent"
    role: str = ""
    instructions: str = ""
    output_model: type[T]

    def __init__(self, llm: LLM) -> None:
        self.llm = llm

    @property
    def system_prompt(self) -> str:
        return f"{ALL_RULES}\n\nYOUR ROLE: {self.role}\n\n{self.instructions}".strip()

    def run(self, prompt: str) -> T:
        return self.llm.generate(system=self.system_prompt, prompt=prompt, output_model=self.output_model)
