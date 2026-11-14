# Provenance and design decisions

Reviewed 2026-11-14. This skill is an original synthesis of research methods and primary provider documentation. No upstream executable code, full skill text, branding or personal traveller profiles were copied. Source review is not an executed provider benchmark. Recheck licences before copying any third-party implementation in a future extension.

## Method donors

- **Borski Travel Hacking Toolkit** — https://github.com/borski/travel-hacking-toolkit ; inspected strategy https://github.com/borski/travel-hacking-toolkit/blob/main/plugins/travel-hacking-toolkit/skills/flight-search-strategy/SKILL.md . Repository identifies MIT. Useful ideas: separate adapters/reference knowledge, multiple fare constructions, eligible specialist channels. Do not inherit its universal provider hierarchy, automatic every-source searches, or universal awards/US-card assumptions.
- **Flyblock Flight Search Harness** — https://github.com/flyblock/flight-search-harness ; workflow https://github.com/flyblock/flight-search-harness/blob/main/docs/search-workflow.md . Apache-2.0. Useful ideas: persistent observations, explicit quote stages, alternative gateways, break-even route challenges and bidirectional route exploration. Its documentation states adults-only support and excludes some common access costs by default. This skill instead requires actual-party demographics and an explicit complete cost scope.
- **Ryunana Adaptive Travel Planner** — https://github.com/ryunana/adaptive-travel-planner-skill/blob/main/SKILL.md . Repository identifies MIT. Useful ideas: capability checks, official operational evidence versus traveller experience, hard feasibility gates and fatigue. Generalize its mainland-China focus through country-specific source discovery.
- **Skywain Trip Planner** — https://github.com/skywain/trip-planner-skill/blob/main/SKILL.md . Repository identifies MIT. Useful ideas: verified research-to-itinerary handoff, realistic navigation and incremental replanning. Keep themed rendering downstream of research; do not impose its fixed budget/format on every task.
- **Mtnrabi Travel Agent Skills** — https://github.com/mtnrabi/travel-agent-skills . Repository identifies MIT. Useful ideas: date-range queries, fresh observations, complete-versus-empty search status and consistent coverage reporting. Provider-specific APIs are optional adapters, not a prerequisite; preserve historical observations but reprice current recommendations.
- **Adrianetti Travel Search** — https://github.com/adrianetti/travel-search/blob/main/SKILL.md and https://github.com/adrianetti/travel-search/blob/main/references/price-tools.md . Use the provider inventory as discovery. A standalone licence was not verified in this review. Do not copy approximate-flight deduplication, fixed subjective scoring or unverified zero-cost/access claims.
- **SkillHQ Flight Search** — https://github.com/skillhq/flight-search/blob/main/SKILL.md . Potential browser-adapter reference, not a whole-trip optimization method. Validate interface shortcuts and passenger state after use rather than assuming URLs populated the intended search.

## Original additions

Use a joint whole-trip search before itinerary creation; demographic and room-allocation requirements; source-family coverage; local-language query grammar; conditional uncommon accommodation/transport branches; strict unknown-cost handling; overlapping-package detection; transparent cost/convenience choices; and a deterministic original cost comparator.

Keep the core workflow tool-neutral and source-independent. Attach official-source dates and check real capabilities at runtime so a polished but obsolete adapter cannot silently determine the research scope.

## Current operational cautions grounded in primary sources

- Amadeus Self-Service is deprecated, with official documentation archived July 2026: https://github.com/amadeus4dev/developer-guides . Enterprise availability is a different question.
- Skyscanner's official MCP is partner-gated: https://developers.skyscanner.net/docs/mcp-server . Its initial live search is partial: https://developers.skyscanner.net/docs/flights-live-prices/overview .
- Booking Demand requires managed affiliate access: https://developers.booking.com/demand/docs/getting-started/prerequisites .
- Duffel test mode includes unrealistic synthetic schedules/fares: https://duffel.com/docs/api/overview/test-mode . Live onboarding is documented at https://duffel.com/guides/getting-started .
- Local discovery examples and provider verification references are recorded in sources.md, flights.md and stays-and-ground.md. Availability and a cheaper final quote must still be established for every real trip.
