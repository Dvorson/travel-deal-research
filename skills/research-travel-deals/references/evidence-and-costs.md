# Evidence and cost contract

## Contents

- Evidence stages and query outcomes
- Quote identity and costs
- Comparison helper
- Input example
- Output limitations

## Evidence stages

- `lead`: community post, search snippet, route map, historical/cached calendar or unsupported headline.
- `listing`: dated search result observed, but selected product and required terms have not been established.
- `selected`: actual selected itinerary/unit for the full party, with total and material inclusions identified.
- `terms_checked`: selected offer plus required baggage/bedding, fees, cancellation and eligibility checked.
- `final_review`: current final review/quote page reached without submitting a booking, payment or hold.

These stages describe what was observed. Even final review does not reserve inventory or guarantee a future price. Record `observed_at`, supplier expiry when provided, live/test mode, source URL and what each source proves. A screenshot or JSON response can support evidence, but its format alone does not establish truth.

Track query outcomes separately: `complete`, `empty_complete`, `partial`, `timeout`, `blocked`, `login_required`, `unsupported`, `not_searched`. A booking window not yet open is a distinct availability reason, not a sellout. Track route existence, service on date, and fare for party as separate statements.

## Quote identity and cost scope

Preserve original currency and quote, normalization rate/date/source, seller and underlying supplier, actual dates, party, room/flight product, eligibility, refundability, prepayment and mandatory extras. Demographic ages are authoritative: derive provider-specific adult/child fare categories from its policy rather than silently changing travellers. An airline may charge an adult fare for an older child; that does not change the demographic record.

For complete trips include all relevant categories: transport, lodging, origin access, destination transfers, local transport, mandatory fees, and any required activity/meal category. Partition inclusions precisely; if bags/taxes are already included in transport, do not add them again. Align dates and products before composing offers.

Every amount given to the helper is the entire party's amount for that component, already in the comparison currency. Never multiply a single-seat fare into a group offer. Keep per-person/per-night display prices only in raw evidence. Document any real FX/payment charge before normalization.

Keep uncertain extras unknown. Model estimates separately; unknown is not zero. Separate refundable deposits from spending, and disclose the cash required to cover them. Do not subtract speculative cashback. Report points consumed and their stated valuation separately; cash-only ranking is inadequate for an award comparison.

## Comparison helper

Run:

```bash
python -B scripts/compare_trip_costs.py /absolute/path/trip-quotes.json
```

Use `--now 2026-11-14T12:00:00Z` only for frozen examples/evaluations. For live research use the current time. Input may also come from stdin with `-`.

Supply `base_currency`, `party`, `required_categories`, and `offers`. Party has exactly `adults`, `children_ages`, and `infants`; use a consistent child-age ordering across offers. Currency must already be normalized, because the helper deliberately does not invent FX rates.

The helper retains invalid/incomplete observations while excluding them from verified ranking. It checks party identity, evidence stage/URL, live mode, hard-constraint status, timestamps/expiry, finite nonnegative decimal amounts, complete category coverage and overlap. It keeps deposits separate. It does not fetch or authenticate source evidence, infer omitted cost categories, evaluate schedules, verify room capacity, or discover travel deals.

Use `constraints_ok: true` only after all hard gates are supported. Unknown or failed gates must remain null/false. The helper's `verified_ranked` is a ranking of the supplied evidence assertions, not independent proof.

## Input example

All amounts, dates, names and links below are a synthetic demonstration.

```json
{
  "base_currency": "EUR",
  "party": {"adults": 2, "children_ages": [6, 9], "infants": 0},
  "required_categories": ["transport", "lodging", "origin_access", "destination_transfers"],
  "offers": [{
    "id": "synthetic-package",
    "name": "Illustrative complete family package",
    "party": {"adults": 2, "children_ages": [6, 9], "infants": 0},
    "constraints_ok": true,
    "live": true,
    "evidence_stage": "terms_checked",
    "observed_at": "2026-11-14T11:00:00Z",
    "valid_until": "2026-11-14T13:00:00Z",
    "source_url": "https://example.com/synthetic-quote",
    "hours": "7.5",
    "components": [
      {"label": "Whole-party package", "covers": ["transport", "lodging", "destination_transfers"], "amount": "1800.00", "currency": "EUR", "status": "verified"},
      {"label": "Return airport access", "covers": ["origin_access"], "amount": "70.50", "currency": "EUR", "status": "verified"}
    ],
    "refundables": [
      {"label": "Security deposit", "amount": "200.00", "currency": "EUR", "status": "verified"}
    ]
  }]
}
```

For a missing transfer use `amount: null`, `status: "unknown"`. Do not remove a mandatory category to force a complete total. For a genuinely inapplicable category use `status: "not_applicable"`, amount `"0"`, and a specific `reason`.

`covers` categories must not overlap, even within a component. A package may cover several categories, but none may be separately counted again. Additional categories are permitted. Amounts must be strings (for example `"0.10"`), finite and nonnegative. Negative coupon/credit rows are unsupported: enter the verified net payable component and preserve its discount evidence in the raw ledger.

Every offer requires unique `id`, exact party, `constraints_ok`, `live`, valid evidence stage, timezone-aware `observed_at`, HTTP(S) source URL, and components. `name`, `valid_until`, `hours` and `refundables` are optional. A stated expiry must be after observation and comparison time. Future observations beyond five minutes are rejected. Uncertain deposit details also exclude the offer from the strict ranking; keep it as conditional and resolve the cash requirement.

## Output limitations

`verified_ranked` sorts by complete cash cost, with deterministic ID ties; it does not select a subjective best trip. `other_offers` retain exclusion reasons and known subtotals. Known subtotals can contain estimates and are not complete verified totals.

The script does not invent a universal freshness duration if a supplier provides no expiry. Therefore re-fetch finalists in the present research session, retain original observation times, and say exactly when checked. A source's “no expiry supplied” never means a fare is indefinitely current. The agent must also ensure all component evidence is current, not just a parent bundle timestamp.

Present time, fatigue, cancellation and protection alongside price. Preserve a small set of useful trade-offs rather than forcing them into an arbitrary weighted score.
