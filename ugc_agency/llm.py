"""Cliente de Claude que usan todos los agentes.

Cada llamada usa structured outputs (`messages.parse`) para que la respuesta
llegue como un modelo Pydantic validado.
"""

from __future__ import annotations

import os
from typing import Protocol, TypeVar

import anthropic
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

DEFAULT_MODEL = "claude-opus-5-5"


class LLMError(RuntimeError):
    pass


class LLM(Protocol):
    def generate(self, *, system: str, prompt: str, output_model: type[T]) -> T: ...


class ClaudeLLM:
    """Wrapper fino sobre el SDK oficial de Anthropic."""

    def __init__(
        self,
        model: str | None = None,
        effort: str | None = None,
        max_tokens: int = 16000,
        client: anthropic.Anthropic | None = None,
    ) -> None:
        self.model = model or os.getenv("UGC_MODEL", DEFAULT_MODEL)
        self.effort = effort or os.getenv("UGC_EFFORT", "high")
        self.max_tokens = max_tokens
        self.client = client or anthropic.Anthropic()

    def generate(self, *, system: str, prompt: str, output_model: type[T]) -> T:
        try:
            response = self.client.messages.parse(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system,
                messages=[{"role": "user", "content": prompt}],
                thinking={"type": "adaptive"},
                output_config={"effort": self.effort},
                output_format=output_model,
                # Si un clasificador de seguridad rechaza la petición, la API la
                # reintenta en el modelo recomendado en vez de devolver el rechazo.
                extra_headers={"anthropic-beta": "server-side-fallback-2026-07-01"},
                extra_body={"fallbacks": "default"},
            )
        except anthropic.RateLimitError as e:
            raise LLMError(f"Límite de uso alcanzado, reintenta más tarde: {e}") from e
        except anthropic.APIStatusError as e:
            raise LLMError(f"Error de la API ({e.status_code}): {e.message}") from e
        except anthropic.APIConnectionError as e:
            raise LLMError(f"No se pudo conectar con la API: {e}") from e

        if response.stop_reason == "refusal":
            raise LLMError("El modelo rechazó la petición (stop_reason=refusal).")
        if response.stop_reason == "max_tokens":
            raise LLMError("La respuesta se cortó por max_tokens; sube max_tokens.")
        if response.parsed_output is None:
            raise LLMError("La respuesta no contenía JSON válido para el esquema.")
        return response.parsed_output
