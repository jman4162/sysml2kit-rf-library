"""End-to-end verification of the PAS-native example (needs phased-array-systems)."""

import pytest

pytest.importorskip("phased_array_systems")

from sysml2kit.verify import EngineRegistry, run_verification

from sysml2kit_rf_library import load_model, models_dir

pytestmark = pytest.mark.pas


def test_pas_example_verifies_end_to_end():
    pytest.importorskip("opensatcom")
    model = load_model("satcom-terminal-pas")
    run = run_verification(
        model,
        model_path=models_dir() / "interchange" / "satcom_terminal_pas.json",
        registry=_full_registry(),
    )
    assert len(run.analyses) == 4  # three pasStudy rungs + the crosscheck
    assert all(a.error is None for a in run.analyses)
    verdicts = {v.requirement_id for v in run.requirements}
    assert verdicts == {"REQ-MARGIN", "REQ-EIRP", "REQ-SLL", "REQ-POWER", "REQ-COST"}
    assert all(v.status == "pass" for v in run.requirements)
    assert all(v.margin is not None and v.margin > 0 for v in run.requirements)


def test_entry_point_discovery_finds_pas_engine():
    registry = EngineRegistry.discover()
    assert "phased-array-systems" in registry.names()


def _full_registry():
    registry = EngineRegistry()
    from phased_array_systems.interop import run_pattern_study, run_study

    registry.register("phased-array-systems", run_study, dist="phased-array-systems")
    registry.register(
        "phased-array-systems-pattern", run_pattern_study, dist="phased-array-systems"
    )
    try:
        from opensatcom.interop import run_link

        registry.register("opensatcom-link", run_link, dist="opensatcom")
    except ImportError:
        pass
    return registry


def test_fidelity_ladder_all_policy_reports_spread():
    pytest.importorskip("opensatcom")
    model = load_model("satcom-terminal-pas")
    run = run_verification(
        model,
        model_path=models_dir() / "interchange" / "satcom_terminal_pas.json",
        registry=_full_registry(),
    )
    assert {a.fidelity for a in run.analyses} == {
        "analytic",
        "pattern-cuts",
        "pattern",
        None,  # the opensatcom crosscheck binding declares no rung label
    }
    margins = {v.fidelity: v.actual for v in run.requirements if v.requirement_id == "REQ-MARGIN"}
    # The degeneracy the ladder exists to break: both analytic-gain rungs
    # agree exactly, and only pattern integration moves the margin.
    assert margins["analytic"] == margins["pattern-cuts"]
    assert margins["pattern"] != margins["analytic"]
    spreads = [
        v.spread
        for v in run.requirements
        if v.requirement_id == "REQ-MARGIN" and v.spread is not None
    ]
    assert spreads
    assert max(spreads) < 0.6  # aedl's clear-sky agreement threshold
    assert run.seconds_by_fidelity["pattern"] > run.seconds_by_fidelity["pattern-cuts"]


def test_escalate_policy_stays_in_budget():
    model = load_model("satcom-terminal-pas")
    run = run_verification(
        model,
        model_path=models_dir() / "interchange" / "satcom_terminal_pas.json",
        registry=_full_registry(),
        policy="escalate",
        budget_s=5.0,
    )
    assert run.passed
    escalated = [v for v in run.requirements if v.escalated_from == "analytic"]
    assert escalated
    declared_spend = sum(run.seconds_by_fidelity.values())
    assert declared_spend < 10.0  # the ladder fits the budget with headroom


def test_opensatcom_crosscheck_agrees_with_pas():
    pytest.importorskip("opensatcom")
    model = load_model("satcom-terminal-pas")
    run = run_verification(
        model,
        model_path=models_dir() / "interchange" / "satcom_terminal_pas.json",
        registry=_full_registry(),
    )
    margin_by_engine = {
        v.engine: v.actual
        for v in run.requirements
        if v.requirement_id == "REQ-MARGIN" and v.fidelity in ("pattern", None)
    }
    pas = margin_by_engine["phased-array-systems-pattern"]
    crosscheck = margin_by_engine["opensatcom-link"]
    assert pas is not None
    assert crosscheck is not None
    assert abs(pas - crosscheck) < 0.6
