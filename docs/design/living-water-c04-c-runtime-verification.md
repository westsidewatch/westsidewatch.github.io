# Living Water Candidate 04 — C runtime verification

Commit `7fa1b1af99b3b75699a62ee2064f5d0c90326bcb` replaces the previously unverified C path with a self-contained classic WebGL God Rays runtime.

Acceptance signal in Doré Design: selecting `C · God Rays` must show `C RUNNING · <fps> FPS`; `C ERROR` is a hard failure. The C canvas is independent of D and uses no esm/module/remote runtime dependency.
