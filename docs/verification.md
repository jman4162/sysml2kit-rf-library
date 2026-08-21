# Running verification

With `sysml2kit>=0.3`, `phased-array-systems>=0.14`, and this library
installed, the PAS-native example executes end to end:

```bash
MODEL=$(python -c 'import sysml2kit_rf_library as m; print(m.models_dir())')/interchange/satcom_terminal_pas.json
sysml2kit verify "$MODEL" --report run.json
```

The engine comes from phased-array-systems' `sysml2kit.engines` entry
point; the study payload is the committed
`models/interchange/satcom_terminal_pas.yaml`. All five requirements pass
with margin:

```text
PASS  REQ-MARGIN  link_margin_db  >= 3.0    actual=22.1  margin=+19.1 [must]
PASS  REQ-EIRP    eirp_dbw        >= 40.0   actual=46.0  margin=+6.0  [must]
PASS  REQ-SLL     sll_db          <= -20.0  actual=-25.4 margin=+5.4  [must]
PASS  REQ-POWER   prime_power_w   <= 450.0  actual=368.6 margin=+81.4 [must]
PASS  REQ-COST    total_cost_usd  <= 60000  actual=25600 margin=+34400 [must]
```

Add `--write-back -o annotated.json` to record the metrics and verdicts
into the model itself, with provenance on every written value. The same
flow runs from Python (`sysml2kit.verify.run_verification`) and over MCP
(`requirements_verify`).
