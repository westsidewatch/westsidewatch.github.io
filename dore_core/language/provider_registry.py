from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(frozen=True)
class LanguageProvider:
    id: str
    engine: str
    models: tuple[str, ...] = ()
    runtimes: tuple[str, ...] = ("local",)
    strengths: tuple[str, ...] = ()
    license_gate: str = "required"
    ai_required: bool = False
    lazy: bool = True


@dataclass(frozen=True)
class TranslationRequest:
    source_language: str
    target_language: str
    profile: str = "general"
    runtime: str = "local"
    long_form: bool = False
    browser_preferred: bool = False


class LanguageProviderRegistry:
    """Provider-neutral registry for Doré's native language faculty.

    Product surfaces never bind to engines directly. This registry describes
    available local/browser translation routes; actual model residency stays
    sparse and lazy.
    """

    def __init__(self, providers: Iterable[LanguageProvider] = ()) -> None:
        self._providers: dict[str, LanguageProvider] = {p.id: p for p in providers}

    def register(self, provider: LanguageProvider) -> None:
        self._providers[provider.id] = provider

    def get(self, provider_id: str) -> LanguageProvider | None:
        return self._providers.get(provider_id)

    def all(self) -> tuple[LanguageProvider, ...]:
        return tuple(self._providers.values())

    def routes(self, request: TranslationRequest) -> tuple[LanguageProvider, ...]:
        providers = [p for p in self._providers.values() if not p.ai_required]
        if request.browser_preferred:
            providers.sort(key=lambda p: ("browser" not in p.runtimes, not p.lazy, p.id))
        elif request.long_form:
            providers.sort(key=lambda p: ("long-form" not in p.strengths, not p.lazy, p.id))
        else:
            providers.sort(key=lambda p: (request.runtime not in p.runtimes, not p.lazy, p.id))
        return tuple(providers)


DEFAULT_LANGUAGE_PROVIDERS = LanguageProviderRegistry((
    LanguageProvider(
        id="ctranslate2",
        engine="CTranslate2",
        models=("MADLAD-400", "OPUS-MT/Marian"),
        runtimes=("local", "server"),
        strengths=("long-form", "batch", "quantized", "multilingual"),
    ),
    LanguageProvider(
        id="bergamot",
        engine="Bergamot",
        models=("Bergamot-compatible",),
        runtimes=("browser", "wasm"),
        strengths=("viewport", "alignment", "offline-browser"),
    ),
    LanguageProvider(
        id="argos",
        engine="Argos Translate",
        models=("Argos packages",),
        runtimes=("local",),
        strengths=("offline", "fallback", "package-management"),
    ),
))
