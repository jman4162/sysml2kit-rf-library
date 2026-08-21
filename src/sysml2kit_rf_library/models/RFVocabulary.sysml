package RFVocabulary {
    doc /* Quantity kinds for antenna/RF systems engineering, with canonical units. */
    attribute def Frequency_GHz {
        doc /* Carrier or design frequency. */
    }
    attribute def Bandwidth_MHz {
        doc /* Occupied or instantaneous bandwidth. */
    }
    attribute def Gain_dBi {
        doc /* Antenna gain relative to isotropic. */
    }
    attribute def EIRP_dBW {
        doc /* Effective isotropic radiated power. */
    }
    attribute def GOverT_dBK {
        doc /* Receive figure of merit G/T. */
    }
    attribute def SidelobeLevel_dB {
        doc /* Peak sidelobe level relative to the main beam. */
    }
    attribute def ScanLoss_dB {
        doc /* Gain loss at the scan angle relative to broadside. */
    }
    attribute def LinkMargin_dB {
        doc /* Margin above the required SNR. */
    }
    attribute def NoiseFigure_dB {
        doc /* Cascaded receive noise figure. */
    }
    attribute def AxialRatio_dB {
        doc /* Polarization axial ratio. */
    }
    attribute def ScanAngle_deg {
        doc /* Beam scan angle off broadside. */
    }
    attribute def PrimePower_W {
        doc /* Prime (DC input) power draw. */
    }
    attribute def UnitCost_USD {
        doc /* Recurring unit cost in US dollars. */
    }
}
