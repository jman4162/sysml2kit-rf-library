# The satcom-terminal examples

## SatcomTerminal28GHz (`satcom-terminal-t3001`)

Mirrors the aedl `t3-001` benchmark: a 28 GHz LEO uplink phased-array
ground terminal with the benchmark's published requirement set — worst-case
link margin, sidelobe level, independent link crosscheck, clear-sky and
gain agreement, prime-power and unit-cost ceilings, grating-lobe margin.
Each requirement is satisfied by a part and verified by an analysis, and
its metric keys match the benchmark's evaluator, so
`aedl.interop.requirements_from_specs` can regenerate the task's
requirement set from this model.

## SatcomTerminalPAS (`satcom-terminal-pas`)

The executable one. Its five requirements use metric keys
phased-array-systems actually emits (`link_margin_db`, `eirp_dbw`,
`sll_db`, `prime_power_w`, `total_cost_usd`), and its `pasStudy` analysis
carries a `verificationBinding` naming the `phased-array-systems` engine
with a committed study payload (16x16 Taylor-tapered array, 28 GHz comms
scenario). See [Verification](verification.md) to run it.
