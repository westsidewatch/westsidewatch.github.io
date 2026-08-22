from dore_core_placeholder import note

# This file documents executable acceptance fixtures until the repository is
# packaged as an importable Python module. It intentionally avoids pretending
# the current hyphenated `dore-core/` directory is already a Python package.

MORPHGNT_MATTHEW_1_1_FIXTURE = (
    "010101 N- ----NSF- Βίβλος Βίβλος βίβλος"
)

REQUIRED_TESTS = [
    "parse MorphGNT reference without losing source-native ref",
    "preserve Greek surface separately from lemma",
    "attach morphology provenance",
    "preserve OSHB Hebrew surface",
    "do not silently classify all Daniel/Ezra tokens as Hebrew",
    "fail when textual provenance is absent",
    "fail when analytical provenance is absent",
    "reconcile source and emitted token counts",
]

# Packaging/import wiring is the next engineering step. This placeholder is
# deliberately non-runnable rather than falsely reporting a passing suite.
note = "TEST_SPEC_PENDING_PACKAGE_WIRING"
