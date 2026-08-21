# Changelog

## 0.3.0 — 2026-08-21

- SatcomTerminalPAS's analysis now carries a three-rung fidelity ladder:
  `analyticBinding` (closed-form), `patternCutsBinding` (simulated
  principal-plane cuts), and `patternBinding` (full-pattern integration
  via the new `phased-array-systems-pattern` engine). The bindings are
  named metadata usages typed by a new `metadata def verificationBinding`
  in RFAnalyses, so each rung has a distinct stable id.
- New `linkCrosscheck` analysis verifies the margin requirement through
  `opensatcom-link` with opensatcom's own array and link models
  (`satcom_terminal_opensatcom.yaml`); the pas-marked tests pin the
  cross-stack agreement under 0.6 dB.
- Payload YAMLs are copied next to the `.sysml` files by
  `scripts/regenerate.py`, so `configRef` resolves from the textual
  models too (`sysml2kit verify SatcomTerminalPAS.sysml RFAnalyses.sysml`).
- `scripts/check_parse.py` no longer exempts Verify/Derive/Allocate/
  MetadataUsage: with sysml2kit >= 0.4 they round-trip through text, and
  only OpaqueElement remains parser-exempt.
- `verify` extra floors move to `sysml2kit[parse,verify]>=0.4.0` and
  `phased-array-systems>=0.14`, and gain `opensatcom>=0.8` for the
  cross-check engine.

## 0.2.1 — 2026-08-21

- Regenerated model artifacts with sysml2kit 0.3.1's corrected metadata
  quoting (`engine = "phased-array-systems"`, double quotes).
- New `verify` extra installs everything the executable example needs:
  `pip install "sysml2kit-rf-library[verify]"`.
- `docs/verification.md` named a nonexistent `phased-array-systems>=0.14`;
  corrected to `>=0.13`, and the literal output numbers moved behind the
  `pas`-marked test instead of living unverified in prose.
- `scripts/check_parse.py` now asserts text/JSON element-kind parity per
  file, so a parser regression that drops a kind fails CI.

## Unreleased

- SatcomTerminalPAS: an executable verification example whose five
  requirements use metric keys phased-array-systems emits, bound to the
  `phased-array-systems` engine via `verificationBinding`; the study payload
  ships next to the interchange JSON.
- Docs site at https://jman4162.github.io/sysml2kit-rf-library/.

## 0.1.0 — 2026-08-21

- RFVocabulary, RFParts, RFRequirements, RFAnalyses packages.
- SatcomTerminal28GHz worked example mirroring the aedl t3-001 benchmark.
- Python loader (`load_model`, `models_dir`) over committed interchange JSON.
