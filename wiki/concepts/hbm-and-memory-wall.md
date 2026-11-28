---
title: HBM and the memory wall
type: concept
tier: 1
updated: 2026-11-28
sources: [SPN-1113-02, SPN-1113-09, SPN-1117-07, SPN-1118-05, SPN-1118-04, SPN-1123-02, SPN-1123-06, SPN-1124-08]
---
# HBM and the memory wall
Summary: AI inference is limited by how fast data reaches the compute units, so memory architecture is a design topic, not only a supply topic.

- Edge AI inference drives memory architectures that reduce data movement, power and latency, including processing-in-memory and near-memory computing. [SPN-1113-02, 2026-11-13]
- Larger models and longer context windows strain memory capacity, bandwidth, latency, power and cost, so compute, interconnect and software must be coordinated. [SPN-1113-09, 2026-11-13]
- Samsung is reportedly developing custom HBM4E for Meta, with customer-specific functions in a base die made on its 2 nm process. [SPN-1118-05, 2026-11-18]
- Nvidia is securing memory, substrate and advanced packaging capacity, with TSMC helping to ease the supply gap. [SPN-1118-04, 2026-11-18]
- When memory is scarce, better test, repair and reliability engineering raises the number of usable dies across SRAM, DRAM and HBM. [SPN-1117-07, 2026-11-17]
- (Explainer) HBM stacks DRAM dies vertically next to the processor on an interposer; the "base die" at the bottom of the stack handles the interface, which is why putting customer logic there is notable.
- Tesla cut AI4.5 memory from 32GB to 24GB because memory costs are rising, moving to LPDDR5X; AI5 and AI6 see similar cuts. [SPN-1123-02, 2026-11-23]
- Nagare Labs claims Z2RAM, a vertically stacked memory with SRAM-like speed and higher density. [SPN-1123-06, 2026-11-23]
- SoftBank explored a $1 trillion SK Hynix purchase and dropped it; the idea shows memory is seen as a key part of the AI supply chain. [SPN-1124-08, 2026-11-24]

Related: [[concepts/ai-accelerator-architecture]] · [[concepts/chiplets-and-hybrid-bonding]] · [[ic-design-link/memory-aware-architecture]] · [[companies/samsung]] · [[index]]
