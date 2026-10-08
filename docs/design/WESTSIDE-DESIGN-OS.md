# Westside Design OS

Status: canonical umbrella authority.

Westside Design OS is the only management system for visual tokens across the public site and tool layer. Typography, color, material, spacing, composition primitives and motion tokens belong under this authority. Existing typography/color files are compatibility runtimes during migration; they are not independent management systems.

## Scope contract

1. Global tokens are defaults, not mandatory page values.
2. Every public surface and tool receives a `data-ws-scope`.
3. A scope can override approved semantic tokens locally. A local adjustment must not rewrite `:root`.
4. Component overrides live below their owning scope.
5. Tools use the same OS and may have independent scoped values.
6. Raw font families, palette literals and competing type scales outside Design OS are migration debt and will be blocked after migration.
7. Composition-specific geometry may remain local when it is not a reusable design token.
8. Generated SVG/covers must consume exported Design OS values or declare an explicit immutable-art exception.

## Authority

Canonical source data: `design-system/tokens/westside.tokens.json`.
Scope registry: `design-system/scopes.json`.
Runtime entry: `static/css/westside-design-os.css`.

Legacy `typography-sitewide.css` and `westside-color-authority.css` are imported by the runtime entry while their declarations are progressively generated/migrated. New management must not be added to those files independently.
