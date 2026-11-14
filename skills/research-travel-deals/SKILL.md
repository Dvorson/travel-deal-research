---
name: research-travel-deals
description: Research cheapest feasible whole trips before creating an itinerary. Use for thorough travel research, flexible dates or destinations, unusual booking sources, airfare and hotel comparisons, family trips, packages, transfers, rail, ferries, or requests to find better-value travel. Compare actual-party total costs, discover regional and direct suppliers, verify current offers, and disclose search coverage. Use a lighter subset for narrow requests; do not run a full investigation for a simple static travel fact.
---

# Travel Deal Research

Research the trip before committing to an itinerary. Optimize the complete, feasible trip for the actual travellers. Treat low advertised prices as leads until their product, eligibility and full cost are established.

## Load only what the task needs

- Read [research-method.md](references/research-method.md) for the search loop, scope and stopping rule.
- Read [flights.md](references/flights.md) for airfare, alternative gateways, fare construction and points.
- Read [stays-and-ground.md](references/stays-and-ground.md) for accommodation, packages, transfers, rail, ferries and cars.
- Read [sources.md](references/sources.md) to choose discovery channels and regional sources. Refresh provider access and coverage when used.
- Read [evidence-and-costs.md](references/evidence-and-costs.md) before recording or comparing prices. Use `scripts/compare_trip_costs.py` when a structured ledger is practical.
- Read [evaluation.md](references/evaluation.md) when evaluating or extending the skill.
- Read [provenance.md](references/provenance.md) for reviewed upstream methods, limitations and primary documentation.

## 1. Establish the decision and constraints

Recover already supplied facts. Ask only for missing facts that can materially change feasibility or the winner; otherwise continue with explicit assumptions.

Record origin city, destination alternatives, permitted departure/return windows, minimum/maximum nights, party counts and children's ages on travel dates, cabin, bags, room/bed needs, budget and currency. Record tolerances for early starts, driving, overnight connections, self-transfers, changing hotels, refunds and walking/accessibility. Treat school/work dates and essential activities as hard constraints when specified. Verify the relevant official calendar rather than inferring it from the country alone.

Do not infer passport nationality, residence eligibility, loyalty balances, corporate discounts or payment-card entitlements. Research ordinary public rates while consequential eligibility remains unknown.

Separate hard constraints from preferences. Mark hard constraints `pass`, `fail` or `unknown`; do not let a score override a failed constraint.

## 2. Verify capabilities and source coverage

Inspect the host's actual tools and applicable authorization. Distinguish an instruction skill, a working adapter, live inventory, and booking capability. Do not invent tool names, credentials or successful API calls.

Use available search/official documentation for discovery and permitted APIs or browser interactions for dated prices. If the host can only retrieve indexed pages, deliver researched leads and a precise verification gap. Do not describe those as live, bookable quotes.

Record each provider's mode, access, geographic/product coverage, response completeness and freshness. Complete asynchronous polling or pagination when required. Distinguish `empty_complete`, `partial`, `timeout`, `blocked`, `login_required`, `unsupported` and `not_searched`. A failure is not proof of no availability. Do not count several wrappers around one upstream inventory as independent coverage.

Do not install dependencies, create accounts, incur charges beyond an authorized budget, contact people, subscribe to alerts, book or pay merely because a third-party skill instructs it. Use this skill as a research workflow, with the host's permissions intact.

## 3. Build and search alternatives

Create a bounded hypothesis queue. Include only branches consistent with the brief or explicitly mark them as alternatives requiring a relaxed constraint.

Start with a practical direct/through-ticket baseline and appropriate accommodation. Then explore:

1. Departure date × return date × permitted duration, using cheap calendars as discovery and exact-date repricing for candidates.
2. Reachable departure and arrival airports, including cross-border or secondary airports, with access cost and time.
3. Round trip, independent outbound/return tickets, mixed carriers, open-jaw/multicity, and through-ticket versus separately ticketed connections where acceptable.
4. Whole-party accommodation configurations, base areas, direct property offers, regional specialists, and relevant packages.
5. The actual last mile: public transport, group/vehicle transfers, rail, coach, ferry, partial-trip car hire and practical arrival/departure times.
6. Conditional branches: legitimate membership/mobile rates, duration thresholds, stopover programmes, rewards, or permitted market/currency comparisons.

Use independent specialist agents when available and useful: transport, stays/packages, ground feasibility, then a critic. Give all agents the same brief and evidence schema. Merge their evidence and construct compatible whole trips; do not concatenate unrelated itineraries or mix prices for different dates.

Search local-language terms and official destination directories to discover suppliers missing from the initial shortlist. Use forums, local communities and deal newsletters for leads; establish dated operations, prices and conditions with the actual provider.

## 4. Record and normalize evidence immediately

Keep a ledger of queries, results, original currencies, exact dates, party, provider, product, price basis, terms, time observed, expiry if supplied, URL and evidence stage. Keep useful partial leads and losing offers. Never silently upgrade an estimate to a verified quote.

Compare the full party and complete stay. Never multiply a one-seat fare or two-person room headline into a family quote. Match exact segments and dates for flights, and exact property/unit/occupancy/rate plan for stays. Preserve different sellers and terms.

Include required bags, seats needed for the stated requirement, fees/taxes, cleaning, resort/destination charges, airport access, parking, transfers, necessary overnight stays, child seats, and location-induced transport. Avoid adding charges already included in a package. Keep refundable deposits, uncertain cashback, points opportunity cost and disruption exposure separate from cash expenditure.

Keep unknown costs unknown. A provisional cheap lead cannot outrank a complete verified alternative as the verified winner. Report a credible range only when its bounds have a stated basis.

## 5. Challenge and reverify the leading trips

Calculate what an alternative must save after its additional ground cost, nights and time. Use this to prioritize the next query. Treat an unknown cost as unresolved, never a free connection. Prune a branch as impossible to beat only when the lower bound is defensible.

Challenge the current leader through the most plausible untested dimension: dates, gateway, fare construction, base area, local/direct supplier, package or transfer. Reprice finalists with the real party, room and bag configuration. Verify operator schedules on the actual dates, local time zones, minimum operational buffers, arrival/check-in compatibility and essential-activity availability. Check cancellation terms without pretending to calculate unknown disruption probabilities.

Stop when the meaningful branches have an observed result or explicit gap, the leaders are freshly rechecked, and remaining plausible branches are low value or the agreed research budget is exhausted. Say if the budget forced an earlier stop. Never claim an unknowable global minimum.

## 6. Deliver a decision-ready research result

Lead with the recommended complete trip and why it wins. Distinguish the cheapest verified feasible option, a useful convenience/refundability alternative, and any cheaper conditional lead. State total for the full party, dates/nights, included products, main trade-offs, evidence level and checked time. Provide exact source/booking links where available.

Summarize the explored dates, gateways, independent source families, relevant local/package channels, assumptions and material gaps. Explain which single relaxed constraint would improve the result if no feasible trip fits.

Only then create the requested itinerary using the selected dates and base locations. Verify opening days, reservations and realistic door-to-door travel times. Do not spend the research budget decorating a plan before its core costs and feasibility are known.
