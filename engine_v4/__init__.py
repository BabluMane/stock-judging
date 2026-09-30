"""engine_v4 -- clean-room implementation of V4_SPEC.md (frozen 2026-09-30).

Source of truth: engine_v4/V4_SPEC.md. Nothing here re-derives, reinterprets or
tunes a frozen rule. Where the spec is silent the code carries a `SPEC-SILENT:`
comment (grep for it) and the PR lists every one; where the spec conflicts with
itself the code raises SpecGapError rather than choosing.
"""
ENGINE_VERSION = "engine v4.0"
SPEC = "V4_SPEC.md (frozen 2026-09-30)"
