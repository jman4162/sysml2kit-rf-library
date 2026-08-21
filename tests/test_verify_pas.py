"""End-to-end verification of the PAS-native example (needs phased-array-systems)."""

import pytest

pytest.importorskip("phased_array_systems")

from sysml2kit.verify import EngineRegistry, run_verification

from sysml2kit_rf_library import load_model, models_dir

pytestmark = pytest.mark.pas


def test_pas_example_verifies_end_to_end():
    model = load_model("satcom-terminal-pas")
    registry = EngineRegistry()
    from phased_array_systems.interop import run_study

    registry.register("phased-array-systems", run_study, dist="phased-array-systems")
    run = run_verification(
        model,
        model_path=models_dir() / "interchange" / "satcom_terminal_pas.json",
        registry=registry,
    )
    assert len(run.analyses) == 1
    assert run.analyses[0].error is None
    verdicts = {v.requirement_id: v for v in run.requirements}
    assert set(verdicts) == {"REQ-MARGIN", "REQ-EIRP", "REQ-SLL", "REQ-POWER", "REQ-COST"}
    assert all(v.status == "pass" for v in verdicts.values())
    assert all(v.margin is not None and v.margin > 0 for v in verdicts.values())


def test_entry_point_discovery_finds_pas_engine():
    registry = EngineRegistry.discover()
    assert "phased-array-systems" in registry.names()
