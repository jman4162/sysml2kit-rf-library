"""Regenerate the committed model artifacts from ``_build.py``.

Writes, with stable UUIDv5 ids so regeneration diffs cleanly:

- ``models/interchange/rf_library.json`` — the four library packages
- ``models/interchange/satcom_terminal_t3001.json`` — library + example
- ``models/*.sysml`` — one textual file per package, for humans and other tools
- ``models/*.yaml`` — engine payload copies, so configRef resolves from the
  textual models too (the originals live next to the interchange JSON)

CI runs this and fails if ``git diff`` is dirty afterward.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from sysml2kit.interchange import write_json
from sysml2kit.text import write_package

from sysml2kit_rf_library._build import build_example, build_library, build_pas_example


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

    pas_example = build_pas_example()
    pas_example.assign_stable_ids()
    write_json(pas_example, models / "interchange" / "satcom_terminal_pas.json")

    for source in (example, pas_example):
        for root_id in source.roots:
            package = source.elements[root_id]
            path = models / f"{package.declared_name}.sysml"
            text = write_package(source, package)
            if not path.exists() or path.read_text() != text:
                path.write_text(text)
                print(f"wrote {package.declared_name}.sysml")
    for payload in sorted((models / "interchange").glob("*.yaml")):
        copy = models / payload.name
        if not copy.exists() or copy.read_text() != payload.read_text():
            copy.write_text(payload.read_text())
            print(f"wrote {payload.name} (payload copy)")
    print("wrote interchange/{rf_library,satcom_terminal_t3001,satcom_terminal_pas}.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
