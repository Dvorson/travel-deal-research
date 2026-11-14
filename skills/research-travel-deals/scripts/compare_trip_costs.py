#!/usr/bin/env python3
"""Compare full-party trip expenses; no network, FX conversion, or value scores.

Usage: python compare_trip_costs.py [input.json|-] [--now 2026-11-14T12:00:00Z]
Amounts must already be in base_currency. Refundable deposits are kept separate.
"""

import argparse
from collections import Counter
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, localcontext
import json
import math
import re
import sys
from urllib.parse import urlsplit


STAGES = {"lead", "listing", "selected", "terms_checked", "final_review"}
STATUSES = {"verified", "estimate", "unknown", "not_applicable"}
ZERO = Decimal("0")


def timestamp(value):
    if not isinstance(value, str):
        raise ValueError("must be an ISO timestamp with timezone")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("must be an ISO timestamp with timezone") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError("must include timezone")
    try:
        return result.astimezone(timezone.utc)
    except OverflowError as exc:
        raise ValueError("must be within the supported UTC date range") from exc


def amount(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("must be a nonnegative finite decimal string")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("must be a nonnegative finite decimal string") from exc
    if not result.is_finite() or result < ZERO:
        raise ValueError("must be a nonnegative finite decimal string")
    # Bound malformed inputs without rounding any accepted monetary amount.
    if len(result.as_tuple().digits) > 100 or abs(result.as_tuple().exponent) > 100:
        raise ValueError("decimal precision/exponent exceeds 100")
    return result


def total(values):
    with localcontext() as ctx:
        # Align every accepted exponent without context rounding, including sums
        # of a large integer and a small fractional monetary amount.
        ctx.prec = (max(v.adjusted() for v in values) - min(v.as_tuple().exponent for v in values)
                    + len(str(len(values))) + 3) if values else 28
        return sum(values, ZERO)


def money(value):
    return format(value, "f")


def party(value):
    if not isinstance(value, dict) or set(value) != {"adults", "children_ages", "infants"}:
        raise ValueError("party requires exactly adults, children_ages, infants")
    for key in ("adults", "infants"):
        if type(value[key]) is not int or value[key] < 0:
            raise ValueError(f"party.{key} must be a nonnegative integer")
    ages = value["children_ages"]
    if not isinstance(ages, list) or any(type(x) is not int or not 0 <= x <= 17 for x in ages):
        raise ValueError("party.children_ages must be a list of integer ages 0..17")
    if value["adults"] + value["infants"] + len(ages) == 0:
        raise ValueError("party must contain at least one traveller")
    return value


def names(value, field):
    if not isinstance(value, list) or not value or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f"{field} must be a nonempty list of nonempty strings")
    if len(set(value)) != len(value):
        raise ValueError(f"{field} contains duplicates")
    return value


def compare(data, now):
    if not isinstance(data, dict):
        raise ValueError("input must be an object")
    currency = data.get("base_currency")
    if not isinstance(currency, str) or not re.fullmatch(r"[A-Z]{3}", currency):
        raise ValueError("base_currency must be a three-letter uppercase currency code")
    request_party = party(data.get("party"))
    required = names(data.get("required_categories"), "required_categories")
    offers = data.get("offers")
    if not isinstance(offers, list):
        raise ValueError("offers must be a list")
    ids = Counter(o.get("id") for o in offers if isinstance(o, dict) and isinstance(o.get("id"), str))
    verified, other = [], []
    for index, offer in enumerate(offers):
        reasons, cost_values, deposit_values, coverage = [], [], [], Counter()
        if not isinstance(offer, dict):
            other.append({"id": f"invalid-{index}", "reasons": ["offer must be an object"], "known_subtotal": "0", "cash_total": None})
            continue
        identifier = offer.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            reasons.append("missing or invalid id")
            identifier = f"invalid-{index}"
        elif ids[identifier] > 1:
            reasons.append("duplicate id")
        try:
            if party(offer.get("party")) != request_party:
                reasons.append("party does not exactly match request")
        except ValueError as exc:
            reasons.append(str(exc))
        if offer.get("constraints_ok") is not True:
            reasons.append("hard constraints failed" if offer.get("constraints_ok") is False else "hard constraints unknown or invalid")
        if offer.get("live") is not True:
            reasons.append("sandbox, non-live, or live status unknown")
        stage = offer.get("evidence_stage")
        if not isinstance(stage, str) or stage not in STAGES:
            reasons.append("invalid evidence_stage")
        elif stage in {"lead", "listing"}:
            reasons.append("evidence has not reached a selected offer")
        try:
            source = urlsplit(offer.get("source_url", ""))
            if source.scheme not in {"https", "http"} or not source.hostname or source.username or source.password:
                raise ValueError()
        except (ValueError, TypeError, AttributeError):
            reasons.append("source_url must be an HTTP(S) evidence URL without credentials")
        observed = None
        try:
            observed = timestamp(offer.get("observed_at"))
            if observed - now > timedelta(minutes=5):
                reasons.append("observed_at is more than five minutes in the future")
        except ValueError as exc:
            reasons.append(f"observed_at {exc}")
        if offer.get("valid_until") is not None:
            try:
                expiry = timestamp(offer["valid_until"])
                if expiry <= now:
                    reasons.append("offer expired")
                if observed is not None and expiry <= observed:
                    reasons.append("valid_until must follow observed_at")
            except ValueError as exc:
                reasons.append(f"valid_until {exc}")
        hours = offer.get("hours")
        if hours is not None:
            try:
                hours = money(amount(str(hours)))
            except ValueError:
                reasons.append("hours must be finite and nonnegative")
                hours = None
        for field, collected in (("components", cost_values), ("refundables", deposit_values)):
            entries = offer.get(field, [] if field == "refundables" else None)
            if not isinstance(entries, list) or (field == "components" and not entries):
                reasons.append(f"{field} must be a list" + (" with at least one component" if field == "components" else ""))
                continue
            for item_index, entry in enumerate(entries):
                prefix = f"{field}[{item_index}]"
                if not isinstance(entry, dict):
                    reasons.append(f"{prefix} must be an object")
                    continue
                if not isinstance(entry.get("label"), str) or not entry["label"].strip():
                    reasons.append(f"{prefix} needs a label")
                if field == "components":
                    try:
                        coverage.update(names(entry.get("covers"), f"{prefix}.covers"))
                    except ValueError as exc:
                        reasons.append(str(exc))
                elif "covers" in entry:
                    reasons.append(f"{prefix}: refundable deposits must not cover expense categories")
                status = entry.get("status")
                if not isinstance(status, str) or status not in STATUSES:
                    reasons.append(f"{prefix} has invalid status")
                elif status in {"estimate", "unknown"}:
                    reasons.append(f"{prefix} is {status}")
                parsed = None
                if entry.get("amount") is None:
                    reasons.append(f"{prefix} amount is unknown")
                else:
                    try:
                        parsed = amount(entry["amount"])
                    except ValueError as exc:
                        reasons.append(f"{prefix} amount {exc}")
                if entry.get("currency") != currency:
                    reasons.append(f"{prefix} currency must equal {currency}; no implicit FX conversion")
                elif parsed is not None:
                    collected.append(parsed)
                if status == "not_applicable" and (parsed != ZERO or not isinstance(entry.get("reason"), str) or not entry["reason"].strip()):
                    reasons.append(f"{prefix} not_applicable requires amount zero and a reason")
        for category in required:
            if coverage[category] == 0:
                reasons.append(f"missing cost category: {category}")
        for category, count in coverage.items():
            if count > 1:
                reasons.append(f"overlapping cost category: {category} ({count} components)")
        reasons = list(dict.fromkeys(reasons))
        expense, deposits = total(cost_values), total(deposit_values)
        row = {"id": identifier, "name": offer.get("name", identifier), "party": offer.get("party"),
               "currency": currency, "cash_total": None if reasons else money(expense),
               "known_subtotal": money(expense), "refundable_deposits": offer.get("refundables", []),
               "known_deposit_subtotal": money(deposits), "hours": hours,
               "source_url": offer.get("source_url"), "evidence_stage": stage,
               "observed_at": offer.get("observed_at"), "valid_until": offer.get("valid_until"),
               "components": offer.get("components"), "reasons": reasons}
        (other if reasons else verified).append(row)
    verified.sort(key=lambda row: (Decimal(row["cash_total"]), row["id"]))
    for rank, row in enumerate(verified, 1):
        row["rank"] = rank
    return {"base_currency": currency, "party": request_party, "as_of": now.isoformat(),
            "required_categories": required, "verified_ranked": verified, "other_offers": other,
            "subtotal_note": "Subtotals sum parsable base-currency amounts, including estimates; they are not complete validated prices. Refundable deposits are excluded from cash_total.",
            "verification_note": "Validation checks supplied evidence metadata, not websites. No automatic age limit is inferred when valid_until is absent; recheck prices before booking."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-", help="JSON file, or - for stdin")
    parser.add_argument("--now", help="ISO timestamp with timezone; default current UTC time")
    args = parser.parse_args()
    try:
        now = timestamp(args.now) if args.now else datetime.now(timezone.utc)
        def reject_constant(value):
            raise ValueError(f"invalid JSON constant: {value}")
        def finite_float(value):
            parsed = float(value)
            if not math.isfinite(parsed):
                raise ValueError("JSON number is outside finite float range; monetary amounts must be strings")
            return parsed
        if args.input == "-":
            data = json.load(sys.stdin, parse_constant=reject_constant, parse_float=finite_float)
        else:
            with open(args.input, encoding="utf-8") as handle:
                data = json.load(handle, parse_constant=reject_constant, parse_float=finite_float)
        print(json.dumps(compare(data, now), indent=2, ensure_ascii=False, allow_nan=False))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
