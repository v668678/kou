"""Core normalization logic."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
import unicodedata

from .mappings import CATEGORY_ALIASES, CONDITION_ALIASES, HEADER_ALIASES

OUTPUT_FIELDS = ["item_id", "category", "brand", "model", "condition", "quantity", "unit_price", "currency", "serial_number", "imei", "notes", "validation_errors"]


def canonical_text(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).strip()
    return re.sub(r"\s+", " ", text)


def canonical_key(value: object) -> str:
    return canonical_text(value).lower().replace("-", "_").replace(" ", "_")


def build_header_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for canonical, aliases in HEADER_ALIASES.items():
        for alias in aliases | {canonical}:
            lookup[canonical_key(alias)] = canonical
    return lookup


HEADER_LOOKUP = build_header_lookup()


def remap_headers(row: Mapping[str, object]) -> dict[str, str]:
    remapped = {field: "" for field in OUTPUT_FIELDS if field != "validation_errors"}
    for raw_key, raw_value in row.items():
        canonical = HEADER_LOOKUP.get(canonical_key(raw_key))
        if canonical:
            remapped[canonical] = canonical_text(raw_value)
    return remapped


def map_alias(value: str, groups: Mapping[str, set[str]], fallback: str) -> str:
    normalized = canonical_text(value).lower()
    for canonical, aliases in groups.items():
        if normalized in {canonical_text(alias).lower() for alias in aliases}:
            return canonical
    return fallback


def normalize_category(value: str) -> str:
    return map_alias(value, CATEGORY_ALIASES, "other")


def normalize_condition(value: str) -> str:
    return map_alias(value, CONDITION_ALIASES, canonical_text(value).upper())


def normalize_quantity(value: str) -> tuple[str, str | None]:
    text = canonical_text(value).replace(",", "")
    try:
        number = int(text)
    except (TypeError, ValueError):
        return text, "quantity must be an integer"
    if number <= 0:
        return str(number), "quantity must be greater than zero"
    return str(number), None


def parse_decimal(value: str) -> Decimal:
    cleaned = canonical_text(value)
    cleaned = re.sub(r"[¥￥$€£,\s]", "", cleaned)
    return Decimal(cleaned)


def normalize_price(value: str, source_currency: str, target_currency: str | None, rate: Decimal | None) -> tuple[str, str, str | None]:
    try:
        price = parse_decimal(value)
    except (InvalidOperation, ValueError):
        return canonical_text(value), source_currency, "unit_price must be numeric"
    if price < 0:
        return str(price), source_currency, "unit_price must not be negative"
    currency = canonical_text(source_currency).upper()
    if target_currency:
        if rate is None or rate <= 0:
            return str(price), currency, "a positive conversion rate is required"
        price = (price * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        currency = canonical_text(target_currency).upper()
    else:
        price = price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return format(price, "f"), currency, None


def mask_identifier(value: str, visible: int = 4) -> str:
    text = canonical_text(value)
    if not text:
        return ""
    if len(text) <= visible:
        return "*" * len(text)
    return "*" * (len(text) - visible) + text[-visible:]


def normalize_row(row: Mapping[str, object], *, default_currency: str = "JPY", target_currency: str | None = None, rate: Decimal | None = None, mask_identifiers: bool = False) -> dict[str, str]:
    result = remap_headers(row)
    errors: list[str] = []
    result["category"] = normalize_category(result["category"])
    result["condition"] = normalize_condition(result["condition"])
    quantity, quantity_error = normalize_quantity(result["quantity"] or "1")
    result["quantity"] = quantity
    if quantity_error:
        errors.append(quantity_error)
    source_currency = result["currency"] or default_currency
    price, currency, price_error = normalize_price(result["unit_price"], source_currency, target_currency, rate)
    result["unit_price"] = price
    result["currency"] = currency
    if price_error:
        errors.append(price_error)
    if not result["model"]:
        errors.append("model is required")
    if result["condition"] not in {"NEW", "A", "B", "C", "D", "PARTS"}:
        errors.append("condition is not recognized")
    if len(result["currency"]) != 3:
        errors.append("currency must be a three-letter code")
    if mask_identifiers:
        result["serial_number"] = mask_identifier(result["serial_number"])
        result["imei"] = mask_identifier(result["imei"])
    result["validation_errors"] = " | ".join(errors)
    return {field: result.get(field, "") for field in OUTPUT_FIELDS}


def normalize_rows(rows: Iterable[Mapping[str, object]], **kwargs: object) -> list[dict[str, str]]:
    return [normalize_row(row, **kwargs) for row in rows]
