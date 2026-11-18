# Shared evidence visibility and display annotations

Legacy inherited overlays previously bypassed evidence filtering and could remain visible in observed mode. They now use the same five-mode display policy as the main scene. The entire overlay is inferred regardless of its legacy material colors: visible in all/inferred modes, hidden in observed/reconstructed/disputed modes. Filtering before generation and changing modes after generation follow the same rule. Phase-hidden layers remain hidden. Filter changes refresh inheritance diagnostics and the current scene note without moving timeline position.

The common helper preserves the existing main-scene evidence semantics. It does not promote inferred content to observed, change source confidence or rewrite shared object events. Overlay geometry, retention ratios, trace IDs and transforms remain unchanged and restore exactly.

The four early-era scene generators now explicitly annotate 21 remaining display components: four approximate spring markers, sixteen disputed support tiers, and one disputed royal location symbol. Their existing IDs and confidence are retained. They have phase-local annotation roles, sourceObjectId=null, semanticCityObject=false and geometryVerified=false. No canonical city records or lifecycle/survival links are fabricated for these symbols. Their visibility continues using the shared confidence policy through the scene adapter.

Foundation inspection adds displayAnnotationComponents; these components remain unbound city objects with their separate display purpose accounted for. Runtime annotation snapshots expose role, confidence and visibility without allowing callers to mutate scene metadata. This explains the previously remaining early-era 1/1/9/10 unbound components; it does not certify archaeological location, buildings or ancient ground.

The new CI test exercises all five modes on all four real early generators and three real inherited overlays, including filter-before-generation, phase suppression precedence, exact restoration, no fabricated core object and defensive annotation snapshots. Browser regression verifies observed-mode overlay withdrawal, all-mode return at the same timeline position, trace consistency and early annotation counts across 18 eras. Full foundation acceptance and step 1 remain incomplete.

No additional external data, image, terrain or model service request is introduced. A small local JS helper module is added; no measured token/FPS/bandwidth saving is claimed. Architecture detail remains paused.
