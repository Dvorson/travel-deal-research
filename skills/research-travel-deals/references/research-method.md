# Research method

## Search contract

Write a small structured brief. Record required facts already known; mark the remainder as an assumption, material question, or optional preference. Use the traveller's actual timezone and ages at the travel date. Distinguish home city from selected airport. Record whether a budget is per person or for everybody.

Define a cost scope. For a whole trip, include main transport, accommodation, access, necessary local travel and mandatory fees. Add food, activities and insurance only to the extent requested or necessary to compare offers fairly; expose excluded discretionary spending. For a flight-only question, still include route-dependent access and mandatory ancillaries if comparing gateways.

Honor a supplied research budget. Otherwise prioritize high-impact unknowns. Do not arbitrarily stop after a fixed number of websites. Do not create a future monitoring task unless requested.

## Joint trip search

Represent a candidate as an internally consistent bundle: dates, nights, gateways, transport products, base areas, rooms, and ground legs. A low flight price is insufficient to choose dates before looking at stay costs.

Maintain a small set of nondominated candidates across verified cash total, door-to-door time, refundability and practical burden. A candidate is dominated only when it is no better on the dimensions the traveller cares about. Do not invent a universal numerical utility score or monetize a child's sleep without user preferences.

Explore the permitted date-duration region. A calendar scan is a screen; requery promising exact combinations. When a tool limits search depth for broad queries, partition into origin/arrival subsets or date bands and refine promising cells. Do not assume a broad query exhaustively searched every combination.

Record each hypothesis:

```json
{
  "question": "Does a different departure gateway reduce total family cost?",
  "branch": "alternate_gateway",
  "status": "not_searched",
  "constraints": ["return before school resumes", "max 3 hours home-to-airport"],
  "sources_planned": ["calendar discovery", "carrier", "rail operator"],
  "evidence_ids": [],
  "next_action": "price gateway access before deeper airfare search"
}
```

## Three passes

### A. Establish a credible baseline

Find a practical return journey and suitable stay for the actual party. Check enough ground transport to know that it works. Record the full quote basis and missing information. This is a benchmark, not a stopping point.

### B. Expand high-value dimensions

Choose independent inventory families rather than interfaces to the same feed. A thorough flight search normally uses broad discovery, a complementary source with different coverage, and direct carrier checks. Add specialist charters, packages, local providers or rewards when relevant.

For accommodation, investigate suitable room configurations and base areas before sorting by nightly price. Include a local/direct discovery path where available. For transfers, identify the actual operator rather than stopping at a map's estimate.

Test structural differences one at a time when useful so the reason for a saving is visible. Combine compatible improvements and reprice the complete bundle.

### C. Challenge the winner

Ask a critic to identify the most promising missing alternative and the most consequential unsupported claim. Give the critic the brief, coverage and raw ledger. Request targeted follow-up research rather than another polished itinerary.

Compare the finalist with its direct supplier and another genuinely different eligible channel where feasible. Direct does not automatically mean cheaper. Distinguish verified price from a convenience preference.

## Adaptive effort and stopping

Prioritize likely decision changes. A regional inventory source may be worth more than a tenth global OTA. A failed source may warrant one changed query or fallback, then an explicit gap; repeated identical retries add no coverage.

Compute break-even budgets. If a baseline is EUR 2,400 and an alternate airport adds EUR 220 in actual access/overnight costs, the alternative's other components must cost under EUR 2,180 to save cash. This is hypothetical arithmetic, not an observed offer. Present extra time separately.

Use bounds honestly. Known nonnegative extras may establish a lower bound; a made-up expected fare cannot. An incomplete price below the baseline remains a lead. If a flight saves EUR 100 but stays cost EUR 160 more on its dates, whole-trip cash cost increases EUR 60.

Finish when all hard constraints have a supported status, relevant structural branches have results or explicit gaps, and comparable finalists are freshly rechecked. Stop sooner only when the resource budget requires it, and disclose that limit.

Use “lowest verified total I found within these dates and sources.” Avoid “all websites checked,” “guaranteed cheapest,” or “bookable” when only a search snippet was seen.

## Handoff

Pass the chosen bundle, required reservations, offer expiry, uncertainty and practical constraints to the itinerary planner. Keep sensitive identity/payment information out of research queries. Retain a researched alternative in case the leading offer reprices or sells out.
