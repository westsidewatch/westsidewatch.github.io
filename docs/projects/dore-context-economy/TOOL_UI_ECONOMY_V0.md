# Tool / UI Economy v0

Status: implemented

## Boundary

Large build logs, test logs, browser/accessibility dumps and other tool output are evidence, not authority. They must not be injected into Codex unbounded.

## Rules

1. Small output passes unchanged.
2. Large output keeps bounded head + tail and records omitted byte count.
3. Browser text/accessibility evidence uses an independent bounded budget.
4. Successful verification may be reused only while all declared input fingerprints are unchanged.
5. Failed verification is never reusable.
6. Any changed input invalidates verified state.
7. Visual acceptance is not inferred from a cached build/test PASS. UI visual acceptance remains a separate gate.

This layer is local and dependency-free. It introduces no hosted Jev/API cost.

## Expected effect

This attacks the second context source after repository reads: repeated logs, browser dumps and repeated verification evidence. Savings are reported only by the paired benchmark; no theoretical percentage is treated as achieved.
