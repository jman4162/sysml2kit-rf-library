"""Authoritative construction of the RF model library.

This module is the source of truth. The committed ``.sysml`` files and
interchange JSON under ``models/`` are generated from it by
``scripts/regenerate.py`` (CI checks they are in sync). Building with the
sysml2kit builder keeps full fidelity — attribute values, units, and
relationship kinds — which a text parse cannot yet guarantee.

The example terminal mirrors the aedl ``t3-001`` benchmark: a 28 GHz LEO
uplink phased-array ground terminal with its published requirement set.
"""

from __future__ import annotations

from sysml2kit.model import Element, Model, builder


def build_vocabulary(model: Model) -> Element:
    """RFVocabulary: attribute definitions with canonical units."""
    pkg = builder.pkg(
        model,
        "RFVocabulary",
        doc="Quantity kinds for antenna/RF systems engineering, with canonical units.",
    )
    quantities = [
        ("Frequency_GHz", "GHz", "Carrier or design frequency."),
        ("Bandwidth_MHz", "MHz", "Occupied or instantaneous bandwidth."),
        ("Gain_dBi", "dBi", "Antenna gain relative to isotropic."),
        ("EIRP_dBW", "dBW", "Effective isotropic radiated power."),
        ("GOverT_dBK", "dBK", "Receive figure of merit G/T."),
        ("SidelobeLevel_dB", "dB", "Peak sidelobe level relative to the main beam."),
        ("ScanLoss_dB", "dB", "Gain loss at the scan angle relative to broadside."),
        ("LinkMargin_dB", "dB", "Margin above the required SNR."),
        ("NoiseFigure_dB", "dB", "Cascaded receive noise figure."),
        ("AxialRatio_dB", "dB", "Polarization axial ratio."),
        ("ScanAngle_deg", "deg", "Beam scan angle off broadside."),
        ("PrimePower_W", "W", "Prime (DC input) power draw."),
        ("UnitCost_USD", None, "Recurring unit cost in US dollars."),
    ]
    for name, unit, doc in quantities:
        builder.attr_def(model, name, owner=pkg, unit=unit, doc=doc)
    return pkg


def build_parts(model: Model) -> Element:
    """RFParts: part and port definitions for phased-array terminals."""
    pkg = builder.pkg(
        model,
        "RFParts",
        doc="Part and port definitions for phased-array antenna systems.",
    )
    builder.port_def(model, "RFPort", owner=pkg, doc="Guided-wave RF interface.")
    builder.port_def(model, "BeamPort", owner=pkg, doc="Formed-beam signal interface.")
    builder.port_def(model, "CtrlPort", owner=pkg, doc="Command and telemetry interface.")
    parts = [
        ("AntennaElement", "A single radiating element."),
        ("RadiatingAperture", "The element lattice as one aperture."),
        ("TRModule", "Transmit/receive module: PA, LNA, phase shifter, switch."),
        ("Beamformer", "Analog, digital, or hybrid beamforming network."),
        ("PhasedArrayAntenna", "Aperture, T/R modules, and beamformer as one antenna."),
        ("RFFrontEnd", "Up/down conversion and filtering between antenna and modem."),
        ("Modem", "Waveform modulation and demodulation."),
        ("SatcomTerminal", "A complete ground terminal."),
    ]
    for name, doc in parts:
        builder.part_def(model, name, owner=pkg, doc=doc)
    return pkg


def build_requirement_defs(model: Model) -> Element:
    """RFRequirements: requirement definitions carrying the metricKey convention.

    Each definition documents which ``metricKey`` its usages set, so
    ``sysml2kit.interop.extract_requirements`` can hand them to a requirements
    engine (phased-array-systems, aedl) without RF knowledge in the kit.
    """
    pkg = builder.pkg(
        model,
        "RFRequirements",
        doc=(
            "Requirement definitions for RF terminals. Usages own attributes "
            "metricKey (str), threshold (number with unit), op (>=, <=, ==), and "
            "optionally severity (must/should/nice); sysml2kit.interop reads them."
        ),
    )
    defs = [
        ("EirpRequirement", "Minimum effective isotropic radiated power."),
        ("GOverTRequirement", "Minimum receive figure of merit."),
        ("SidelobeRequirement", "Maximum pattern sidelobe level."),
        ("ScanLossRequirement", "Maximum gain loss at the scan-angle extreme."),
        ("LinkMarginRequirement", "Minimum worst-case link margin."),
        ("BandwidthRequirement", "Minimum instantaneous bandwidth."),
        ("PowerCeilingRequirement", "Maximum prime-power draw."),
        ("CostCeilingRequirement", "Maximum recurring unit cost."),
        ("CrosscheckRequirement", "Maximum disagreement between independent analyses."),
        ("GratingLobeRequirement", "Minimum grating-lobe margin in wavelengths."),
    ]
    for name, doc in defs:
        builder.req_def(model, name, owner=pkg, doc=doc)
    return pkg


def build_analyses(model: Model) -> Element:
    """RFAnalyses: analysis case definitions that verification links point at."""
    pkg = builder.pkg(
        model,
        "RFAnalyses",
        doc="Analysis case definitions; bindings to physics engines live downstream.",
    )
    cases = [
        ("LinkBudgetAnalysis", "Worst-case link closure over an evaluation envelope."),
        ("ArrayPatternAnalysis", "Full pattern integration: gain, sidelobes, grating lobes."),
        ("ScanPerformanceAnalysis", "Gain and pattern degradation across the scan envelope."),
        ("SwapCostAnalysis", "Prime power and recurring cost rollup."),
    ]
    for name, doc in cases:
        builder.analysis_def(model, name, owner=pkg, doc=doc)
    builder.metadata_def(
        model,
        "verificationBinding",
        owner=pkg,
        doc=(
            "Binds an analysis case to a physics engine by registry name. "
            "Reserved keys: engine, configRef, payload.<dotted>, fidelity, "
            "costSeconds (see the sysml2kit SPEC)."
        ),
    )
    return pkg


def build_library() -> Model:
    """Build the four library packages in one model."""
    model = Model()
    build_vocabulary(model)
    build_parts(model)
    build_requirement_defs(model)
    build_analyses(model)
    return model


def _metric_requirement(
    model: Model,
    owner: Element,
    short: str,
    name: str,
    *,
    definition: Element,
    text: str,
    metric_key: str,
    op: str,
    threshold: float,
    unit: str | None,
    severity: str = "must",
) -> Element:
    req = builder.req(model, short, name, owner=owner, text=text, definition=definition)
    builder.attr(model, "metricKey", metric_key, owner=req)
    builder.attr(model, "threshold", threshold, owner=req, unit=unit)
    builder.attr(model, "op", op, owner=req)
    builder.attr(model, "severity", severity, owner=req)
    return req


def _defs(model: Model) -> dict[str, Element]:
    return {el.declared_name: el for el in model.iter_elements() if el.declared_name}


def _add_example(model: Model) -> Model:
    defs = _defs(model)
    pkg = builder.pkg(
        model,
        "SatcomTerminal28GHz",
        doc=(
            "28 GHz LEO uplink phased-array ground terminal, mirroring the aedl "
            "t3-001 benchmark: close the worst-case link over the evaluation "
            "envelope inside a 450 W prime-power and 45 kUSD unit-cost ceiling."
        ),
    )
    pkg.imports = ["RFVocabulary::*", "RFParts::*", "RFRequirements::*", "RFAnalyses::*"]

    terminal = builder.part(model, "terminal", owner=pkg, definition=defs["SatcomTerminal"])
    array = builder.part(model, "array", owner=terminal, definition=defs["PhasedArrayAntenna"])
    builder.attr(model, "frequency", 28.0, owner=array, unit="GHz", source="t3-001 brief")
    builder.attr(model, "bandwidth", 50.0, owner=array, unit="MHz", source="t3-001 brief")
    builder.attr(model, "maxScanAngle", 60.0, owner=array, unit="deg", source="t3-001 envelope")
    builder.part(
        model,
        "elements",
        owner=array,
        definition=defs["AntennaElement"],
        multiplicity="[1..*]",
    )
    builder.part(
        model, "trModules", owner=array, definition=defs["TRModule"], multiplicity="[1..*]"
    )
    beamformer = builder.part(model, "beamformer", owner=array, definition=defs["Beamformer"])
    front_end = builder.part(model, "frontEnd", owner=terminal, definition=defs["RFFrontEnd"])
    builder.part(model, "modem", owner=terminal, definition=defs["Modem"])
    beam_out = builder.port(model, "beamOut", owner=beamformer, definition=defs["BeamPort"])
    fe_in = builder.port(model, "beamIn", owner=front_end, definition=defs["BeamPort"])
    builder.connect(model, beam_out, fe_in, owner=terminal, name="beamFeed")

    reqs = [
        (
            "REQ-LINK-MARGIN",
            "WorstCaseLinkMargin",
            defs["LinkMarginRequirement"],
            "The link shall close (margin >= 0 dB) worst-case over the evaluation envelope.",
            "worst_case_link_margin_db",
            ">=",
            0.0,
            "dB",
            "must",
        ),
        (
            "REQ-SLL",
            "PatternSidelobes",
            defs["SidelobeRequirement"],
            "Worst-case pattern sidelobe level shall not exceed -16 dB.",
            "worst_case_pattern_sll_db",
            "<=",
            -16.0,
            "dB",
            "must",
        ),
        (
            "REQ-INDEP-LINK",
            "IndependentLinkClosure",
            defs["LinkMarginRequirement"],
            "The link shall also close under the independent opensatcom recomputation.",
            "opensatcom_worst_case_margin_db",
            ">=",
            0.0,
            "dB",
            "must",
        ),
        (
            "REQ-CLEARSKY-AGREE",
            "ClearSkyAgreement",
            defs["CrosscheckRequirement"],
            "Clear-sky margins from the two link analyses shall agree within 1.2 dB.",
            "crosscheck_clearsky_margin_disagreement_db",
            "<=",
            1.2,
            "dB",
            "should",
        ),
        (
            "REQ-GAIN-XCHECK",
            "GainCrosscheck",
            defs["CrosscheckRequirement"],
            "Claimed and integrated gain shall agree within 0.5 dB.",
            "crosscheck_gain_disagreement_db",
            "<=",
            0.5,
            "dB",
            "should",
        ),
        (
            "REQ-POWER",
            "PrimePowerCeiling",
            defs["PowerCeilingRequirement"],
            "Prime power draw shall not exceed 450 W.",
            "prime_power_w",
            "<=",
            450.0,
            "W",
            "must",
        ),
        (
            "REQ-COST",
            "UnitCostCeiling",
            defs["CostCeilingRequirement"],
            "Recurring unit cost shall not exceed 45,000 USD from the parts table.",
            "unit_cost_usd",
            "<=",
            45000.0,
            None,
            "must",
        ),
        (
            "REQ-GRATING",
            "GratingLobeMargin",
            defs["GratingLobeRequirement"],
            "The lattice shall keep grating lobes out of visible space over the scan envelope.",
            "grating_margin_lambda",
            ">=",
            0.0,
            None,
            "must",
        ),
    ]
    req_elements = {}
    for short, name, definition, text, key, op, threshold, unit, severity in reqs:
        req_elements[short] = _metric_requirement(
            model,
            pkg,
            short,
            name,
            definition=definition,
            text=text,
            metric_key=key,
            op=op,
            threshold=threshold,
            unit=unit,
            severity=severity,
        )

    link_budget = builder.analysis(
        model,
        "linkBudget",
        owner=pkg,
        definition=defs["LinkBudgetAnalysis"],
        subject=terminal,
        objective="Close the uplink worst-case over the t3-001 evaluation envelope.",
    )
    pattern = builder.analysis(
        model,
        "patternAnalysis",
        owner=pkg,
        definition=defs["ArrayPatternAnalysis"],
        subject=array,
        objective="Integrate the full pattern; recompute gain, sidelobes, grating margin.",
    )
    swap = builder.analysis(
        model,
        "swapCost",
        owner=pkg,
        definition=defs["SwapCostAnalysis"],
        subject=terminal,
        objective="Roll up prime power and unit cost from the parts table.",
    )

    for short, satisfier in [
        ("REQ-LINK-MARGIN", terminal),
        ("REQ-INDEP-LINK", terminal),
        ("REQ-SLL", array),
        ("REQ-GRATING", array),
        ("REQ-POWER", terminal),
        ("REQ-COST", terminal),
    ]:
        builder.satisfy(model, source=satisfier, target=req_elements[short], owner=pkg)

    for short, part in [
        ("REQ-SLL", array),
        ("REQ-GRATING", array),
        ("REQ-POWER", terminal),
    ]:
        builder.allocate(model, source=req_elements[short], target=part, owner=pkg)

    for short, analysis_usage in [
        ("REQ-LINK-MARGIN", link_budget),
        ("REQ-INDEP-LINK", link_budget),
        ("REQ-CLEARSKY-AGREE", link_budget),
        ("REQ-SLL", pattern),
        ("REQ-GAIN-XCHECK", pattern),
        ("REQ-GRATING", pattern),
        ("REQ-POWER", swap),
        ("REQ-COST", swap),
    ]:
        builder.verify(model, source=analysis_usage, target=req_elements[short], owner=pkg)

    return model


def build_example() -> Model:
    """Build the library plus the SatcomTerminal28GHz example package."""
    model = build_library()
    return _add_example(model)


def _add_pas_example(model: Model) -> Model:
    """Add the SatcomTerminalPAS package: an executable verification example.

    Unlike SatcomTerminal28GHz (which mirrors the aedl t3-001 benchmark and
    its metric names), this example's requirements use the metric keys
    phased-array-systems actually emits, and its analysis carries a
    fidelity ladder of ``verificationBinding`` metadata so ``sysml2kit
    verify`` runs real studies: ``analytic`` (closed-form gain),
    ``pattern-cuts`` (simulated principal-plane cuts, gain still composed
    analytically), and ``pattern`` (full-pattern integration feeding the
    link recompute). A second analysis cross-checks the margin requirement
    against the independent ``opensatcom-link`` engine.
    """
    defs = _defs(model)
    pkg = builder.pkg(
        model,
        "SatcomTerminalPAS",
        doc=(
            "28 GHz LEO uplink terminal sized for verification closure: a "
            "16x16 Taylor-tapered array whose study the phased-array-systems "
            "engine executes, checking margin, EIRP, sidelobes, power, and cost."
        ),
    )
    pkg.imports = ["RFVocabulary::*", "RFParts::*", "RFRequirements::*", "RFAnalyses::*"]

    terminal = builder.part(model, "terminal", owner=pkg, definition=defs["SatcomTerminal"])
    array = builder.part(model, "array", owner=terminal, definition=defs["PhasedArrayAntenna"])
    builder.attr(model, "frequency", 28.0, owner=array, unit="GHz")
    builder.attr(model, "elementsX", 16, owner=array)
    builder.attr(model, "elementsY", 16, owner=array)
    builder.attr(model, "taperSidelobeTarget", -25.0, owner=array, unit="dB")

    reqs = [
        (
            "REQ-MARGIN",
            "LinkMarginFloor",
            "LinkMarginRequirement",
            "The link shall close with at least 3 dB margin at the nominal point.",
            "link_margin_db",
            ">=",
            3.0,
            "dB",
        ),
        (
            "REQ-EIRP",
            "EirpFloor",
            "EirpRequirement",
            "EIRP shall be at least 40 dBW.",
            "eirp_dbw",
            ">=",
            40.0,
            "dBW",
        ),
        (
            "REQ-SLL",
            "SidelobeCeiling",
            "SidelobeRequirement",
            "Pattern sidelobes shall not exceed -20 dB.",
            "sll_db",
            "<=",
            -20.0,
            "dB",
        ),
        (
            "REQ-POWER",
            "PrimePowerCeiling",
            "PowerCeilingRequirement",
            "Prime power draw shall not exceed 450 W.",
            "prime_power_w",
            "<=",
            450.0,
            "W",
        ),
        (
            "REQ-COST",
            "CostCeiling",
            "CostCeilingRequirement",
            "Recurring cost shall not exceed 60,000 USD.",
            "total_cost_usd",
            "<=",
            60000.0,
            None,
        ),
    ]
    req_elements = {}
    for short, name, def_name, text, key, op, threshold, unit in reqs:
        req_elements[short] = _metric_requirement(
            model,
            pkg,
            short,
            name,
            definition=defs[def_name],
            text=text,
            metric_key=key,
            op=op,
            threshold=threshold,
            unit=unit,
        )

    study = builder.analysis(
        model,
        "pasStudy",
        owner=pkg,
        definition=defs["LinkBudgetAnalysis"],
        subject=terminal,
        objective="Evaluate the terminal study with phased-array-systems.",
    )
    # Fidelity ladder: three bindings on one analysis, ordered by declared
    # cost. The first two share the analytic gain composition (their link
    # margins are identical by construction); only the pattern-integration
    # rung moves the margin, which is why the ladder needs it.
    binding_def = defs["verificationBinding"]
    builder.metadata(
        model,
        study,
        {
            "engine": "phased-array-systems",
            "configRef": "satcom_terminal_pas.yaml",
            "payload.antenna_fidelity": "analytic",
            "fidelity": "analytic",
            "costSeconds": 0.001,
        },
        name="analyticBinding",
        definition=binding_def,
    )
    builder.metadata(
        model,
        study,
        {
            "engine": "phased-array-systems",
            "configRef": "satcom_terminal_pas.yaml",
            "payload.antenna_fidelity": "pattern",
            "fidelity": "pattern-cuts",
            "costSeconds": 0.01,
        },
        name="patternCutsBinding",
        definition=binding_def,
    )
    builder.metadata(
        model,
        study,
        {
            "engine": "phased-array-systems-pattern",
            "configRef": "satcom_terminal_pas.yaml",
            "fidelity": "pattern",
            "costSeconds": 1.0,
        },
        name="patternBinding",
        definition=binding_def,
    )
    for req_usage in req_elements.values():
        builder.verify(model, source=study, target=req_usage, owner=pkg)

    # Independent margin cross-check: same requirement, different physics
    # stack (opensatcom's link engine with its own antenna and propagation
    # models). Disagreement between the two engines is the error bar.
    crosscheck = builder.analysis(
        model,
        "linkCrosscheck",
        owner=pkg,
        definition=defs["LinkBudgetAnalysis"],
        subject=terminal,
        objective="Recompute the link margin independently with opensatcom.",
    )
    builder.metadata(
        model,
        crosscheck,
        {"engine": "opensatcom-link", "configRef": "satcom_terminal_opensatcom.yaml"},
        name="crosscheckBinding",
        definition=binding_def,
    )
    builder.verify(model, source=crosscheck, target=req_elements["REQ-MARGIN"], owner=pkg)
    for short, satisfier in [
        ("REQ-MARGIN", terminal),
        ("REQ-EIRP", array),
        ("REQ-SLL", array),
        ("REQ-POWER", terminal),
        ("REQ-COST", terminal),
    ]:
        builder.satisfy(model, source=satisfier, target=req_elements[short], owner=pkg)
    return model


def build_pas_example() -> Model:
    """Build the library plus the executable SatcomTerminalPAS package."""
    model = build_library()
    return _add_pas_example(model)
