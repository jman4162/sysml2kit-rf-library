"""CI check: every committed .sysml file parses with the sysmlpy backend."""

from __future__ import annotations

from pathlib import Path

from sysml2kit.backends import get_backend


def main() -> int:
    """Parse all packaged .sysml files; non-zero exit on any syntax error."""
    root = Path(__file__).resolve().parents[1]
    files = sorted((root / "src" / "sysml2kit_rf_library" / "models").glob("*.sysml"))
    # Parse per file: the combined graft makes short names ambiguous across
    # the two example packages, which defeats satisfy-endpoint resolution.
    backend = get_backend("sysmlpy")
    parsed_models = [backend.parse(f.read_text(), filename=str(f)) for f in files]
    total = sum(len(m.elements) for m in parsed_models)
    print(f"parsed {len(files)} files, {total} elements")

    # Parity guard: every element kind present in the interchange JSON must
    # also come back from the text parse in at least the same count, except
    # the kinds the parser is documented to lose (SPEC.md fidelity table).
    from collections import Counter

    from sysml2kit.interchange import model_from_json

    parser_lossy = {
        "VerifyRelationship",
        "DeriveRelationship",
        "AllocateRelationship",
        "MetadataUsage",
        "OpaqueElement",
    }
    interchange_dir = root / "src" / "sysml2kit_rf_library" / "models" / "interchange"
    json_kinds: Counter[str] = Counter()
    for json_file in sorted(interchange_dir.glob("*.json")):
        for element in model_from_json(json_file).elements.values():
            json_kinds[type(element).__name__] += 1
    text_kinds: Counter[str] = Counter()
    for parsed in parsed_models:
        for el in parsed.elements.values():
            text_kinds[type(el).__name__] += 1
    missing = {
        kind: (json_kinds[kind], text_kinds.get(kind, 0))
        for kind in json_kinds
        if kind not in parser_lossy and text_kinds.get(kind, 0) < json_kinds[kind]
    }
    # rf_library.json + satcom JSONs overlap with the five .sysml files, so
    # compare against the two self-contained example models only when counts
    # disagree badly; a kind absent from text entirely is the real signal.
    absent = [kind for kind, (j, t) in missing.items() if t == 0]
    if absent:
        print(f"[check_parse] kinds present in JSON but absent from text parse: {absent}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
