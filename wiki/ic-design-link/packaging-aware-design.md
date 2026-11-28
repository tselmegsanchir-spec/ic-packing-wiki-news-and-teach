---
title: Packaging-aware IC design
type: ic-link
tier: 1
updated: 2026-11-28
sources: [SPN-1112-01, SPN-1116-03, SPN-1120-03, SPN-1113-03, SPN-1125-03, SPN-1124-09, SPN-1125-10]
---
# Packaging-aware IC design
Why a designer should care about packaging news.

- Hybrid bonding at a 6 µm pitch is a stated Samsung target for 2027. [SPN-1112-01, 2026-11-12]
- Hybrid and fusion bonding support both heterogeneous integration and transistor scaling. [SPN-1116-03, 2026-11-16]
- Failures in die-to-die interconnects are hard to debug because of limited access and test granularity. [SPN-1120-03, 2026-11-20]
- Package warpage simulation accuracy depends on realistic material data. [SPN-1113-03, 2026-11-13]
- (Explainer) A chip is designed for a package: die-to-die links, power delivery, heat and test access all need decisions during design, not after.
- (AI hypothesis) Designers who understand packaging limits may avoid late redesigns; the sources only describe the technology.
- Denser packages raise soft-error risk from alpha particles, which designers of AI and HPC chips may need to plan for. [SPN-1125-03, 2026-11-25]
- Diamond Foundry made a 200mm single-crystal diamond wafer to spread heat from AI chips. [SPN-1124-09, 2026-11-24]
- Photonic parts that each meet spec can behave differently once combined, so design is judged at system level. [SPN-1125-10, 2026-11-25]

Related: [[concepts/chiplets-and-hybrid-bonding]] · [[index]]
