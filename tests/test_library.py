from sysml2kit.interop import extract_requirements
from sysml2kit.model import PartUsage, RequirementUsage
from sysml2kit.query import trace_matrix, unverified_requirements
from sysml2kit.validation import validate

from sysml2kit_rf_library import MODELS, load_model, models_dir
from sysml2kit_rf_library._build import build_example, build_library

EXPECTED_METRICS = {
    "worst_case_link_margin_db": (">=", 0.0),
    "worst_case_pattern_sll_db": ("<=", -16.0),
    "opensatcom_worst_case_margin_db": (">=", 0.0),
    "crosscheck_clearsky_margin_disagreement_db": ("<=", 1.2),
    "crosscheck_gain_disagreement_db": ("<=", 0.5),
    "prime_power_w": ("<=", 450.0),
    "unit_cost_usd": ("<=", 45000.0),
    "grating_margin_lambda": (">=", 0.0),
}


def test_packaged_models_load():
    for name in MODELS:
        model = load_model(name)
        assert model.elements


def test_committed_artifacts_match_build():
    from sysml2kit.interchange import model_to_json

    rebuilt = build_example()
    rebuilt.assign_stable_ids()
    assert model_to_json(load_model("satcom-terminal-t3001")) == model_to_json(rebuilt)


def test_library_validates_clean():
    issues = validate(load_model("rf-library"))
    assert not [i for i in issues if i.severity == "error"]


def test_example_validates_clean():
    issues = validate(load_model("satcom-terminal-t3001"))
    assert not [i for i in issues if i.severity == "error"]
    # No pint-unparseable units either: the vocabulary sticks to real units.
    assert not [i for i in issues if i.rule_id == "S2K006"]


def test_extraction_yields_t3001_requirement_set():
    specs = extract_requirements(load_model("satcom-terminal-t3001"))
    assert {s.metric_key: (s.op, s.value) for s in specs} == EXPECTED_METRICS


def test_every_requirement_is_verified():
    model = load_model("satcom-terminal-t3001")
    assert unverified_requirements(model) == []


def test_traceability_matrix_covers_array():
    model = load_model("satcom-terminal-t3001")
    matrix = trace_matrix(model)
    array = next(p for p in model.iter_elements(kind=PartUsage) if p.declared_name == "array")
    sll = next(
        r for r in model.iter_elements(kind=RequirementUsage) if r.declared_short_name == "REQ-SLL"
    )
    marks = matrix.cells[(str(sll.element_id), str(array.element_id))]
    assert marks == {"satisfy", "allocate"}


def test_sysml_files_exist_for_every_package():
    names = {p.stem for p in models_dir().glob("*.sysml")}
    assert names == {
        "RFVocabulary",
        "RFParts",
        "RFRequirements",
        "RFAnalyses",
        "SatcomTerminal28GHz",
        "SatcomTerminalPAS",
    }


def test_library_build_is_deterministic():
    from sysml2kit.interchange import model_to_json

    a, b = build_library(), build_library()
    a.assign_stable_ids()
    b.assign_stable_ids()
    assert model_to_json(a) == model_to_json(b)
