from __future__ import annotations

from collections.abc import Iterable

from .model import CapabilityManifest


class CapabilityRegistry:
    """Compact registry for dormant Doré capabilities.

    Only manifests live here. Heavy instructions/providers stay behind refs and
    are not imported or loaded by registry construction.
    """

    def __init__(self, manifests: Iterable[CapabilityManifest] = ()) -> None:
        self._items: dict[str, CapabilityManifest] = {}
        for manifest in manifests:
            self.register(manifest)

    def register(self, manifest: CapabilityManifest) -> None:
        if manifest.id in self._items:
            raise ValueError(f"duplicate capability id: {manifest.id}")
        self._items[manifest.id] = manifest

    def get(self, capability_id: str) -> CapabilityManifest:
        return self._items[capability_id]

    def all(self) -> tuple[CapabilityManifest, ...]:
        return tuple(self._items[k] for k in sorted(self._items))

    def __len__(self) -> int:
        return len(self._items)


def default_registry() -> CapabilityRegistry:
    """Small first registry proving one Doré, many dormant visual capabilities."""
    return CapabilityRegistry([
        CapabilityManifest(
            id="visual.direct",
            faculty="visual",
            description="Resolve product need into visual intent and constraints.",
            triggers=("visual", "hero", "illustration", "poster", "website image"),
            outputs=("visual_brief",),
            verification=("brief-complete",),
        ),
        CapabilityManifest(
            id="visual.grammar",
            faculty="visual",
            description="Retrieve or build Doré visual grammar and recipe.",
            triggers=("style", "grammar", "dore original", "visual language"),
            inputs=("visual_brief",), outputs=("style_recipe",),
            verification=("originality", "product-fit"),
        ),
        CapabilityManifest(
            id="image.generate",
            faculty="visual",
            description="Generate raster or illustrative candidate assets using a lazy renderer.",
            triggers=("generate image", "create image", "illustration", "hero art"),
            inputs=("visual_brief", "style_recipe"), outputs=("asset_candidate",),
            requires=("renderer",), provider_refs=("local-image-renderer",),
            verification=("render-exists", "provenance"), latency_class="slow",
            instruction_ref="dore-image/SKILL.md",
        ),
        CapabilityManifest(
            id="image.critic",
            faculty="visual",
            description="Inspect image candidate for brief accuracy, coherence, quality and product fit.",
            triggers=("critique image", "inspect image", "review candidate"),
            inputs=("asset_candidate",), outputs=("critique_result",),
            verification=("scored-review",), instruction_ref="dore-image/SKILL.md",
        ),
        CapabilityManifest(
            id="design.compose",
            faculty="visual",
            description="Compose approved assets, typography and layout in Doré Design shared workspace.",
            triggers=("layout", "compose", "insert asset", "design page"),
            inputs=("asset_candidate",), outputs=("design_patch",),
            instruction_ref="dore-design/PROJECT.md",
        ),
        CapabilityManifest(
            id="design.verify",
            faculty="visual",
            description="Verify structured render, responsive behavior and export constraints.",
            triggers=("verify design", "responsive", "export check"),
            inputs=("design_patch",), outputs=("verification_result",),
            verification=("responsive", "render", "export"),
            instruction_ref="dore-design/PROJECT.md",
        ),
    ])
