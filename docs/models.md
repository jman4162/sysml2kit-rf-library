# The models

Load any packaged model by name:

```python
from sysml2kit_rf_library import MODELS, load_model, models_dir

print(sorted(MODELS))   # rf-library, satcom-terminal-pas, satcom-terminal-t3001
model = load_model("rf-library")
print(models_dir())     # the packaged .sysml and interchange files
```

## Library packages

- **RFVocabulary** — attribute definitions with canonical units:
  Frequency_GHz, Bandwidth_MHz, Gain_dBi, EIRP_dBW, GOverT_dBK,
  SidelobeLevel_dB, ScanLoss_dB, LinkMargin_dB, NoiseFigure_dB,
  AxialRatio_dB, ScanAngle_deg, PrimePower_W, UnitCost_USD.
- **RFParts** — part definitions (AntennaElement, RadiatingAperture,
  TRModule, Beamformer, PhasedArrayAntenna, RFFrontEnd, Modem,
  SatcomTerminal) and ports (RFPort, BeamPort, CtrlPort).
- **RFRequirements** — requirement definitions whose usages carry the
  `metricKey` convention (`metricKey`, `threshold` with unit, `op`,
  `severity`), so `sysml2kit.interop.extract_requirements` hands them to a
  requirements engine mechanically.
- **RFAnalyses** — analysis case definitions (LinkBudgetAnalysis,
  ArrayPatternAnalysis, ScanPerformanceAnalysis, SwapCostAnalysis) that
  verify links point at.

## Consuming from the command line or agents

```bash
sysml2kit show "$(python -c 'import sysml2kit_rf_library as m; print(m.models_dir())')/interchange/satcom_terminal_pas.json" --traceability
```

Over MCP, sysml2kit's `library_load` tool writes any packaged model as an
interchange JSON file for an agent to work on.
