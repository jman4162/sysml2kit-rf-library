# Running verification

With `sysml2kit>=0.4`, `phased-array-systems>=0.14`, and this library
installed (`pip install "sysml2kit-rf-library[verify]"`), the PAS-native
example executes end to end:

```bash
MODEL=$(python -c 'import sysml2kit_rf_library as m; print(m.models_dir())')/interchange/satcom_terminal_pas.json
sysml2kit verify "$MODEL" --report run.json
```

All five requirements pass with positive margin (the exact numbers track
phased-array-systems and are asserted in this repo's `pas`-marked tests,
not here):

```text
PASS  REQ-MARGIN  link_margin_db  >= 3.0    [must] @analytic
PASS  REQ-EIRP    eirp_dbw        >= 40.0   [must] @analytic
PASS  REQ-SLL     sll_db          <= -20.0  [must] @analytic
PASS  REQ-POWER   prime_power_w   <= 450.0  [must] @analytic
PASS  REQ-COST    total_cost_usd  <= 60000  [must] @analytic
```

Add `--write-back -o annotated.json` to record the metrics and verdicts
into the model itself, with provenance on every written value. The same
flow runs from Python (`sysml2kit.verify.run_verification`) and over MCP
(`requirements_verify`).

## The fidelity ladder

`SatcomTerminalPAS::pasStudy` carries three sibling bindings, each a
named `metadata` usage typed by `RFAnalyses::verificationBinding`:

| binding | engine | rung (`fidelity`) | what moves |
|---|---|---|---|
| `analyticBinding` | `phased-array-systems` | `analytic` | closed-form gain, design-value sidelobes |
| `patternCutsBinding` | `phased-array-systems` | `pattern-cuts` | simulated principal-plane sidelobes; gain still composed analytically |
| `patternBinding` | `phased-array-systems-pattern` | `pattern` | full-pattern integration feeds the link recompute |

The first two rungs report bit-identical link margins by construction —
both compose gain as directivity minus scan, taper, and quantization
losses. Only the `pattern` rung integrates the radiation pattern and
re-runs the link budget with the integrated gain, so the margin actually
responds to pattern-level effects. On this terminal the analytic rungs
report 22.135 dB and the pattern rung 22.197 dB, a 0.06 dB gain
disagreement; the per-requirement `spread` in the report is that honest
error bar.

The default `--policy all` runs every rung. `--policy cheapest` runs one.
`--policy escalate --budget-s 5` runs the cheapest rungs, ranks
must-requirements by margin thinness, and escalates within the declared
`costSeconds` budget; escalated verdicts carry `escalated_from` and the
report records measured `seconds_by_fidelity`.

## The independent cross-check

A second analysis, `linkCrosscheck`, verifies the same margin requirement
through the `opensatcom-link` engine (payload
`satcom_terminal_opensatcom.yaml`, opensatcom's own PAM array gain and
link chain — an independent physics stack, not a replay). With the
conventions mirrored (total power, feed loss, and system noise
temperature composed as T_ant + 290 (F − 1)), the two stacks agree to
0.10 dB on this terminal; the `pas`-marked test pins the agreement under
0.6 dB, aedl's clear-sky threshold.

## From the textual notation

The same verification runs from the `.sysml` files. The typed bindings
resolve against the `metadata def` in `RFAnalyses.sysml`, so pass both
files:

```bash
cd $(python -c 'import sysml2kit_rf_library as m; print(m.models_dir())')
sysml2kit verify SatcomTerminalPAS.sysml RFAnalyses.sysml --policy escalate --budget-s 5
```
