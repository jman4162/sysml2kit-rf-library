"""CI check: every committed .sysml file parses with the sysmlpy backend."""

from __future__ import annotations

from pathlib import Path

from sysml2kit.backends import get_backend


def main() -> int:
    """Parse all packaged .sysml files; non-zero exit on any syntax error."""
    root = Path(__file__).resolve().parents[1]
    files = sorted((root / "src" / "sysml2kit_rf_library" / "models").glob("*.sysml"))
    model = get_backend("sysmlpy").parse_files(files)
    print(f"parsed {len(files)} files, {len(model.elements)} elements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
