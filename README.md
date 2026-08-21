# sysml2kit-rf-library

[![CI](https://github.com/jman4162/sysml2kit-rf-library/actions/workflows/ci.yml/badge.svg)](https://github.com/jman4162/sysml2kit-rf-library/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/sysml2kit-rf-library)](https://pypi.org/project/sysml2kit-rf-library/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)

A SysML v2 model library for antenna/RF systems engineering, consumed through
[sysml2kit](https://github.com/jman4162/sysml2kit).

The kit stays domain-general; this library carries the RF vocabulary:

- **RFVocabulary** — quantity kinds with canonical units (Frequency_GHz,
  Gain_dBi, EIRP_dBW, GOverT_dBK, SidelobeLevel_dB, ScanLoss_dB,
  LinkMargin_dB, PrimePower_W, ...).
- **RFParts** — part/port definitions: AntennaElement, RadiatingAperture,
  TRModule, Beamformer, PhasedArrayAntenna, RFFrontEnd, Modem, SatcomTerminal.
- **RFRequirements** — requirement definitions carrying the `metricKey`
  convention, so `sysml2kit.interop.extract_requirements` hands them to a
  requirements engine (phased-array-systems, aedl) mechanically.
- **RFAnalyses** — analysis case definitions (link budget, pattern
  integration, scan performance, SWaP-C rollup) that verify links point at.
- **SatcomTerminal28GHz** — a worked example mirroring the aedl `t3-001`
  benchmark: a 28 GHz LEO uplink phased-array ground terminal with its full
  requirement set (worst-case link margin, sidelobes, independent link
  crosscheck, power and cost ceilings, grating-lobe margin), each satisfied
  by a part and verified by an analysis.

## Install and load

```bash
pip install sysml2kit-rf-library
```

```python
from sysml2kit_rf_library import load_model
from sysml2kit.interop import extract_requirements
from sysml2kit.query import trace_matrix

model = load_model("satcom-terminal-t3001")
print(trace_matrix(model).render())
for spec in extract_requirements(model):
    print(spec.id, spec.metric_key, spec.op, spec.value, spec.units)
```

Or inspect it from the command line:

```bash
sysml2kit show src/sysml2kit_rf_library/models/interchange/satcom_terminal_t3001.json --traceability
sysml2kit validate src/sysml2kit_rf_library/models/interchange/*.json
```

## How the repo is organized

`src/sysml2kit_rf_library/_build.py` is the authoritative source: it
constructs the models with the sysml2kit builder, keeping attribute values,
units, and relationship kinds exact. The committed artifacts under
`src/sysml2kit_rf_library/models/` — one `.sysml` file per package for humans
and other tools, plus interchange JSON with stable UUIDv5 ids — are generated
by `scripts/regenerate.py`, and CI fails if they drift from the build.

All content is authored fresh under Apache-2.0; nothing is copied from the
EPL-2.0 OMG model libraries.

## Citation

```bibtex
@software{hodge2026sysml2kitrflibrary,
  author  = {Hodge, John},
  title   = {sysml2kit-rf-library: SysML v2 models for antenna/RF systems engineering},
  year    = {2026},
  url     = {https://github.com/jman4162/sysml2kit-rf-library},
  license = {Apache-2.0}
}
```

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
