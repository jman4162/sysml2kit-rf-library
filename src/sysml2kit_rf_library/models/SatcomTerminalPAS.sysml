package SatcomTerminalPAS {
    public import RFVocabulary::*;
    public import RFParts::*;
    public import RFRequirements::*;
    public import RFAnalyses::*;
    doc /* 28 GHz LEO uplink terminal sized for verification closure: a 16x16 Taylor-tapered array whose study the phased-array-systems engine executes, checking margin, EIRP, sidelobes, power, and cost. */
    part terminal : SatcomTerminal {
        part array : PhasedArrayAntenna {
            attribute frequency = 28.0 [GHz];
            attribute elementsX = 16;
            attribute elementsY = 16;
            attribute taperSidelobeTarget = -25.0 [dB];
        }
    }
    requirement <'REQ-MARGIN'> LinkMarginFloor {
        doc /* The link shall close with at least 3 dB margin at the nominal point. */
        attribute metricKey = "link_margin_db";
        attribute threshold = 3.0 [dB];
        attribute op = ">=";
        attribute severity = "must";
    }
    requirement <'REQ-EIRP'> EirpFloor {
        doc /* EIRP shall be at least 40 dBW. */
        attribute metricKey = "eirp_dbw";
        attribute threshold = 40.0 [dBW];
        attribute op = ">=";
        attribute severity = "must";
    }
    requirement <'REQ-SLL'> SidelobeCeiling {
        doc /* Pattern sidelobes shall not exceed -20 dB. */
        attribute metricKey = "sll_db";
        attribute threshold = -20.0 [dB];
        attribute op = "<=";
        attribute severity = "must";
    }
    requirement <'REQ-POWER'> PrimePowerCeiling {
        doc /* Prime power draw shall not exceed 450 W. */
        attribute metricKey = "prime_power_w";
        attribute threshold = 450.0 [W];
        attribute op = "<=";
        attribute severity = "must";
    }
    requirement <'REQ-COST'> CostCeiling {
        doc /* Recurring cost shall not exceed 60,000 USD. */
        attribute metricKey = "total_cost_usd";
        attribute threshold = 60000.0;
        attribute op = "<=";
        attribute severity = "must";
    }
    analysis pasStudy : LinkBudgetAnalysis {
        subject terminal;
        objective { doc /* Evaluate the terminal study with phased-array-systems. */ }
    }
    metadata analyticBinding : verificationBinding about pasStudy {
        engine = "phased-array-systems";
        configRef = "satcom_terminal_pas.yaml";
        'payload.antenna_fidelity' = "analytic";
        fidelity = "analytic";
        costSeconds = 0.001;
    }
    metadata patternCutsBinding : verificationBinding about pasStudy {
        engine = "phased-array-systems";
        configRef = "satcom_terminal_pas.yaml";
        'payload.antenna_fidelity' = "pattern";
        fidelity = "pattern-cuts";
        costSeconds = 0.01;
    }
    metadata patternBinding : verificationBinding about pasStudy {
        engine = "phased-array-systems-pattern";
        configRef = "satcom_terminal_pas.yaml";
        fidelity = "pattern";
        costSeconds = 1.0;
    }
    dependency verify_1 from pasStudy to LinkMarginFloor;
    dependency verify_2 from pasStudy to EirpFloor;
    dependency verify_3 from pasStudy to SidelobeCeiling;
    dependency verify_4 from pasStudy to PrimePowerCeiling;
    dependency verify_5 from pasStudy to CostCeiling;
    analysis linkCrosscheck : LinkBudgetAnalysis {
        subject terminal;
        objective { doc /* Recompute the link margin independently with opensatcom. */ }
    }
    metadata crosscheckBinding : verificationBinding about linkCrosscheck {
        engine = "opensatcom-link";
        configRef = "satcom_terminal_opensatcom.yaml";
    }
    dependency verify_6 from linkCrosscheck to LinkMarginFloor;
    satisfy LinkMarginFloor by terminal;
    satisfy EirpFloor by terminal.array;
    satisfy SidelobeCeiling by terminal.array;
    satisfy PrimePowerCeiling by terminal;
    satisfy CostCeiling by terminal;
}
