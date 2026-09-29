"""Product-neutral service contract for Doré Language Faculty.

This is the single application-facing entry point for translation planning.
Products such as Dawn Library and Cinema ask Doré for a plan; they never bind
themselves to CTranslate2, Bergamot, Argos, or a model name directly.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .base import LanguageUnit, TextWitness, validate_units
from .provider_registry import DEFAULT_LANGUAGE_PROVIDERS, TranslationRequest


@dataclass(frozen=True)
class TranslationPlan:
    source_language: str
    target_language: str
    profile: str
    runtime: str
    long_form: bool
    browser_preferred: bool
    providers: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


def plan_translation(
    *,
    source_language: str,
    target_language: str = "zh-Hant",
    profile: str = "general",
    runtime: str = "local",
    long_form: bool = False,
    browser_preferred: bool = False,
) -> TranslationPlan:
    request = TranslationRequest(
        source_language=source_language,
        target_language=target_language,
        profile=profile,
        runtime=runtime,
        long_form=long_form,
        browser_preferred=browser_preferred,
    )
    providers = DEFAULT_LANGUAGE_PROVIDERS.routes(request)
    return TranslationPlan(
        source_language=source_language,
        target_language=target_language,
        profile=profile,
        runtime=runtime,
        long_form=long_form,
        browser_preferred=browser_preferred,
        providers=tuple(provider.id for provider in providers),
    )


def validate_translation_input(
    units: Iterable[LanguageUnit], witness: TextWitness
) -> tuple[LanguageUnit, ...]:
    """Materialize and validate provenance before a translation provider runs."""
    materialized = tuple(units)
    errors = validate_units(materialized, witness)
    if errors:
        raise ValueError("invalid translation input: " + ";".join(errors))
    return materialized
