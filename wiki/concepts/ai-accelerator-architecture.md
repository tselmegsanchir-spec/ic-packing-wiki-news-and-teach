---
title: AI accelerator architecture
type: concept
tier: 1
updated: 2026-11-28
sources: [SPN-1113-11, SPN-1113-12, SPN-1113-02, SPN-1116-01, SPN-1123-12]
---
# AI accelerator architecture
Summary: Design choices such as number formats, open ISAs and memory placement are shaped by AI workloads.

- Arm is adding FP8 support; its FPMR register switches between E4M3 and E5M2 formats to cut memory use, power and latency. [SPN-1113-11, 2026-11-13]
- The AI boom pushes chip design toward parallel processing and power efficiency, raising demand for flexible, modular, open hardware, with RISC-V discussed for AI acceleration. [SPN-1113-12, 2026-11-13]
- Processing-in-memory and near-memory computing aim to reduce data movement for edge inference. [SPN-1113-02, 2026-11-13]
- At electronica 2026 chipmakers highlighted MCUs with dedicated NPUs, agentic tools, vertical power delivery and GaN for AI data centers. [SPN-1116-01, 2026-11-16]
- (Explainer) FP8 uses 8 bits per number: E4M3 has more precision, E5M2 has more range, so a chip may switch between them per workload.
- AI accelerators need high current at low voltage, which moves power delivery to vertical designs with regulators near the processor. [SPN-1123-12, 2026-11-23]

Related: [[ic-design-link/memory-aware-architecture]] · [[concepts/hbm-and-memory-wall]] · [[glossary]] · [[index]]
