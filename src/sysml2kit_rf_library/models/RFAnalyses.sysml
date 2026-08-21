package RFAnalyses {
    doc /* Analysis case definitions; bindings to physics engines live downstream. */
    analysis def LinkBudgetAnalysis {
        doc /* Worst-case link closure over an evaluation envelope. */
    }
    analysis def ArrayPatternAnalysis {
        doc /* Full pattern integration: gain, sidelobes, grating lobes. */
    }
    analysis def ScanPerformanceAnalysis {
        doc /* Gain and pattern degradation across the scan envelope. */
    }
    analysis def SwapCostAnalysis {
        doc /* Prime power and recurring cost rollup. */
    }
    metadata def verificationBinding {
        doc /* Binds an analysis case to a physics engine by registry name. Reserved keys: engine, configRef, payload.<dotted>, fidelity, costSeconds (see the sysml2kit SPEC). */
    }
}
