from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .model import CapabilityManifest


@dataclass(frozen=True)
class CapabilitySurface:
    """A thin product surface over a shared Doré core capability.

    Sections do not own duplicate implementations. They only declare where a
    core faculty may emerge, and which local presentation profile it uses.
    """

    section: str
    faculty: str
    profile: str = "default"
    triggers: tuple[str, ...] = ()


class SurfaceRegistry:
    def __init__(self, surfaces: tuple[CapabilitySurface, ...] = ()) -> None:
        self._surfaces = list(surfaces)

    def register(self, surface: CapabilitySurface) -> None:
        if surface not in self._surfaces:
            self._surfaces.append(surface)

    def resolve(self, section: str, faculty: str) -> CapabilitySurface | None:
        for surface in self._surfaces:
            if surface.section == section and surface.faculty == faculty:
                return surface
        for surface in self._surfaces:
            if surface.section == "*" and surface.faculty == faculty:
                return CapabilitySurface(
                    section=section,
                    faculty=faculty,
                    profile=surface.profile,
                    triggers=surface.triggers,
                )
        return None

    def available(self, section: str, manifests: Mapping[str, CapabilityManifest]) -> tuple[CapabilityManifest, ...]:
        faculties = {
            surface.faculty
            for surface in self._surfaces
            if surface.section in ("*", section)
        }
        return tuple(manifest for manifest in manifests.values() if manifest.faculty in faculties)


# Site-wide faculties live once in Doré core. Product areas only choose how
# they surface. Translation is the first explicit shared faculty: Dawn Library
# presents it as reading translation; Doré Folio presents it as writing-side
# translation, while both route to the same core capability.
DEFAULT_SURFACES = SurfaceRegistry((
    CapabilitySurface("*", "translation", "contextual", ("translate", "translation", "翻譯", "翻译")),
    CapabilitySurface("dawn-library", "translation", "reading"),
    CapabilitySurface("dore-folio", "translation", "writing"),
))
