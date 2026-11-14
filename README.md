# Travel Deal Research

An installable agent skill for researching the cheapest **feasible, complete trip** before writing an itinerary. It combines flexible flight searches, overlooked accommodation sources, packages, local operators and realistic ground transport into one evidence-based workflow.

The skill focuses on the actual travel party and total trip cost. A cheap fare with an expensive airport transfer, a room that cannot accommodate the children, or a quote with unknown fees cannot silently become the recommended deal.

## Install

With [Vercel's open Skills CLI](https://github.com/vercel-labs/skills), run:

```bash
npx skills add Dvorson/travel-deal-research --skill research-travel-deals
```

The installer lets you choose a supported agent. It installs into the current project by default. Add `-g` for installation across projects, or select an agent explicitly:

```bash
npx skills add Dvorson/travel-deal-research --skill research-travel-deals -a codex
npx skills add Dvorson/travel-deal-research --skill research-travel-deals -a claude-code
```

The current Skills CLI requires Node.js 22.20 or later. See its [installation documentation](https://github.com/vercel-labs/skills#install-a-skill) for current requirements and options.

For another host that supports the [Agent Skills format](https://agentskills.io/specification), download or clone this repository and install the complete `skills/research-travel-deals` directory using that host's skill installer. Keep its reference documents and script together with `SKILL.md`. This repository is a skill package; it does not install a travel API or grant access to booking inventory.

## Use

Ask your agent to use **Travel Deal Research**, or invoke `$research-travel-deals` in a host that supports named skill invocation.

Example:

> Use Travel Deal Research to compare a 7–10 night family trip in our school holiday window. We are two adults and two children aged 6 and 9, departing from Amsterdam. Consider nearby airports, local accommodation sites, direct property offers and flight-plus-hotel packages. Include luggage, airport access and destination transfers. Avoid self-transfers. Research and show the best complete options before proposing an itinerary.

For a narrower request:

> Use Travel Deal Research to challenge this hotel quote. Check the same room, dates, occupancy and cancellation terms through the property directly, regional booking sites and eligible member rates. Include every mandatory fee and the cost of the location.

The skill scales its research to the request. It does not require a full trip investigation for a simple travel fact.

## What it teaches the agent

- **Search the decision space:** vary departure and return dates, trip length, nearby airports, open-jaw routes, mixed carriers, accommodation bases and room configurations.
- **Look beyond the first aggregators:** discover direct suppliers, regional specialists, local-language terms, tourism directories, package operators and relevant rail, coach and ferry options.
- **Use experienced traveller strategies conditionally:** investigate duration thresholds, whole-party room alternatives, partial-trip car hire, legitimate member or mobile offers, rewards and stopover programmes when they fit the brief.
- **Price the whole trip:** include bags, necessary seats, fees, taxes, cleaning charges, airport access, parking, transfers and necessary overnight stays without double-counting package inclusions.
- **Keep evidence honest:** distinguish indexed leads, selected live quotes, estimates, expired offers, sandbox data, blocked searches and incomplete provider results.
- **Challenge the current leader:** calculate how much an alternative must save after additional transport, nights and time, then spend the next search on the most promising unresolved branch.
- **Respect feasibility:** preserve the exact travel party, room occupancy, hard dates, arrival times, last public transport, check-in requirements and the user's tolerance for travel complexity.
- **Report search coverage:** show what was checked, what remains unresolved, the cheapest verified feasible option and useful alternatives before constructing the itinerary.

No skill can prove the global cheapest available trip. This one makes its search scope and evidence visible so the recommendation can be assessed.

## Requirements and access

The research instructions work with the search, browser or travel tools already available to the host. Current prices require appropriate live access. With indexed search alone, the agent must return researched leads and identify the missing verification.

The optional cost comparator requires **Python 3.10 or later** and uses only the standard library. It makes no network requests, requires no API keys, and performs no bookings or payments. Installing the skill does not enable paid services, accounts, alerts or supplier contact.

Provider access and coverage change. The source registry records a review date and instructs the agent to recheck current capabilities rather than assuming an integration still works.

## Cost comparator

Run the included synthetic example from the repository root:

```bash
python3 skills/research-travel-deals/scripts/compare_trip_costs.py \
  examples/family-quotes.json \
  --now 2026-11-14T12:00:00Z
```

The fixture is deliberately fictional, with reserved `example.com` URLs. Its `live` and verification fields model valid inputs for the tests; they do not describe real offers. The frozen `--now` makes its expiry checks reproducible. Omit `--now` for real work to use current UTC time.

Expected fixture results:

- A complete package ranks first at **EUR 1,870.50**.
- A complete independently booked alternative follows at **EUR 1,990.00**.
- A **EUR 200.00 refundable deposit** remains separate from trip expenditure.
- An incomplete lead with a **EUR 1,350.00 known subtotal** is retained with exclusion reasons and does not enter the verified ranking.

The comparator checks supplied metadata and arithmetic; it does **not** verify websites or establish that an offer exists. Amounts must be decimal strings for the complete party and already converted into the stated base currency. No exchange rate is inferred. Missing or estimated required costs, mismatched parties, overlapping charges and invalid evidence exclude an offer from the strict ranking.

Read the [evidence and input schema](skills/research-travel-deals/references/evidence-and-costs.md) before building a ledger. The output retains incomplete alternatives so the agent can pursue useful leads instead of hiding them.

## Package contents

- [Core skill](skills/research-travel-deals/SKILL.md): the research workflow and decision rules.
- [Research method](skills/research-travel-deals/references/research-method.md): hypothesis queue, coverage and stopping rule.
- [Flights](skills/research-travel-deals/references/flights.md): dates, gateways, fare structures and rewards.
- [Stays and ground transport](skills/research-travel-deals/references/stays-and-ground.md): accommodation, packages, transfers, rail, ferries and cars.
- [Source registry](skills/research-travel-deals/references/sources.md): discovery channels, regional sources and access limitations.
- [Evidence and costs](skills/research-travel-deals/references/evidence-and-costs.md): quote stages, cost treatment and comparator schema.
- [Evaluation guidance](skills/research-travel-deals/references/evaluation.md): realistic tasks and failure cases.
- [Provenance](skills/research-travel-deals/references/provenance.md): reviewed projects, borrowed methods and original additions.
- [Comparator](skills/research-travel-deals/scripts/compare_trip_costs.py), [synthetic example](examples/family-quotes.json) and [regression tests](tests/test_compare_trip_costs.py).

## Development and validation

Run the offline test suite:

```bash
python3 -B -m unittest discover -s tests -v
```

The tests exercise full-party totals, missing and estimated costs, package overlap, invalid parties, sandbox evidence, expiry and timezone boundaries, currency handling, exact decimal arithmetic, refundable deposits and CLI errors. GitHub Actions runs the suite on supported Python versions after pushes and pull requests.

These checks validate the package's deterministic helper. They are not a benchmark of live travel inventory or proof that the research workflow always finds the cheapest trip. See the evaluation guidance for testing the agent workflow itself.

Contributions should preserve the distinction between leads and verified quotes, include a current primary source for provider claims, and add regression coverage for meaningful changes to the comparator. Do not include private traveller data, credentials or real booking references in examples or issues.

## Licence and attribution

[MIT](LICENSE). The skill text and comparator are an original synthesis. The [provenance notes](skills/research-travel-deals/references/provenance.md) credit the reviewed projects and explain which methods were retained or changed. Third-party services and linked projects keep their own terms and licences; this repository does not redistribute their implementations or imply their endorsement.
