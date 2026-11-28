---
title: Chiplets and hybrid bonding
type: concept
tier: 1
updated: 2026-11-28
sources: [SPN-1112-01, SPN-1116-03, SPN-1118-03, SPN-1120-03, SPN-1112-04, SPN-1124-03, SPN-1125-03]
---
# Chiplets and hybrid bonding
Summary: AI chips are increasingly built by stacking or joining several smaller dies; the bonding method decides how fine the connections can be.

- Samsung targets early 2027 to develop 3D Cube-H hybrid bonding with a 6 µm interconnect pitch for AI processors and HBM. [SPN-1112-01, 2026-11-12]
- A paper describes hybrid and fusion wafer bonding as foundational for both "More than Moore" heterogeneous integration and "More Moore" transistor scaling. [SPN-1116-03, 2026-11-16]
- Another paper compares LAB, R-LAB and R-LTC flip-chip bonding for AI/HPC chiplet packages, citing better interconnect quality, warpage control and reliability. [SPN-1118-03, 2026-11-18]
- A paper shows fine-pitch probing (EOTPR) can isolate die-to-die interconnect defects in chiplet devices. [SPN-1120-03, 2026-11-20]
- imec's CEO says AI shifts innovation to system-level integration of logic, memory, photonics and packaging. [SPN-1112-04, 2026-11-12]
- (Explainer) Flip-chip uses solder bumps to connect a die face-down; hybrid bonding joins copper pads directly, allowing a much smaller pitch, so more connections fit between stacked dies.
- (AI hypothesis) As pitch shrinks, designers may need to plan die-to-die interfaces and test access earlier in the design flow; the sources do not say this directly.
- Amkor's S-SWIFT uses embedded-trace RDL to give die-to-die links more bandwidth. [SPN-1124-03, 2026-11-24]
- Alpha-particle emission is a growing soft-error risk as package density rises. [SPN-1125-03, 2026-11-25]

Related: [[concepts/co-packaged-optics]] · [[ic-design-link/packaging-aware-design]] · [[concepts/hbm-and-memory-wall]] · [[glossary]] · [[index]]
