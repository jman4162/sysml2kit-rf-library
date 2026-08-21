# sysml2kit-rf-library

A SysML v2 model library for antenna/RF systems engineering, consumed
through [sysml2kit](https://jman4162.github.io/sysml2kit/).

```bash
pip install sysml2kit-rf-library
```

```python
from sysml2kit_rf_library import load_model

model = load_model("satcom-terminal-pas")
```

The kit stays domain-general; this library carries the RF vocabulary as
model content: quantity kinds with canonical units, part and port
definitions for phased-array terminals, requirement definitions using the
machine-checkable `metricKey` convention, and analysis case definitions.
Two worked satcom-terminal examples show the intended division of labor —
one mirrors the aedl `t3-001` benchmark, the other executes for real
through the phased-array-systems verification engine.

Everything under `models/` is generated from `_build.py` (the source of
truth) with stable ids, committed as both `.sysml` text and interchange
JSON, and kept in sync by CI.
