---
name: automated-financial-competitor-analyst
description: Automatically identifies market competitors and conducts a professional-grade financial analysis report. Benchmarks revenue, market share, and operational efficiency ratios.
---

# Skill: Autonomous Financial Competitor Analysis

This skill allows the agent to act as a Corporate Strategy Lead. It dynamically discovers industry peers and synthesizes real-time financial data into a formal investment-grade report.

## Discovery Workflow
1. **Segment Identification**: Research the target company’s primary revenue drivers (e.g., UPI payments, lending, or insurance).
2. **Peer Discovery**: Use Perplexity to find the top 3-4 direct competitors in that specific segment and geography.
3. **Financial Extraction**: For each competitor, extract:
    - **Top-Line**: Revenue (FY24/25) and CAGR.
    - **Profitability**: EBITDA margins and Net Profit.
    - **Efficiency**: CAC (Customer Acquisition Cost) and LTV if available.
    - **Market Share**: Volume or value-based percentage.

## Search Queries (sonar-deep-research)
- "Identify the top direct competitors of [Company] in the [Region] [Industry] segment as of late 2025."
- "Benchmark the FY2024 and projected FY2025 revenue, EBITDA, and market share for [Target] vs [Competitors]."

## Reporting Structure
The final result saved to the filesystem **must** follow this format:
- **Executive Summary**: 2-sentence market overview.
- **Competitor Landscape**: Why these specific peers were chosen.
- **Benchmarking Table**: A markdown table comparing key financial KPIs.
- **Moat Analysis**: Qualitative assessment of competitive advantages.
- **Sources**: Citations from Perplexity.

## Constraints
- Never rely on 2023 data if 2024/2025 data is available.
- If private, use "Estimated Revenue" or "Latest Valuation."