"""Regenerate the committed model artifacts from ``_build.py``.

Writes, with stable UUIDv5 ids so regeneration diffs cleanly:

- ``models/interchange/rf_library.json`` — the four library packages
- ``models/interchange/satcom_terminal_t3001.json`` — library + example
- ``models/*.sysml`` — one textual file per package, for humans and other tools

CI runs this and fails if ``git diff`` is dirty afterward.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sysml2kit.interchange import write_json
from sysml2kit.text import write_package

from sysml2kit_rf_library._build import build_example, build_library


def main() -> int:
    """Rebuild every committed artifact under models/."""
    root = Path(__file__).resolve().parents[1]
    models = root / "src" / "sysml2kit_rf_library" / "models"
    (models / "interchange").mkdir(parents=True, exist_ok=True)

    library = build_library()
    library.assign_stable_ids()
    write_json(library, models / "interchange" / "rf_library.json")

    example = build_example()
    example.assign_stable_ids()
    write_json(example, models / "interchange" / "satcom_terminal_t3001.json")

    for root_id in example.roots:
        package = example.elements[root_id]
        text = write_package(example, package)
        (models / f"{package.declared_name}.sysml").write_text(text)
        print(f"wrote {package.declared_name}.sysml")
    print("wrote interchange/rf_library.json, interchange/satcom_terminal_t3001.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
