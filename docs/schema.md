# Normalized inventory schema

## Header matching

Input headers are normalized with Unicode NFKC normalization, whitespace cleanup, and case-insensitive matching. Supported aliases include common Japanese, Simplified Chinese, and English supplier terminology.

Unknown columns are ignored in version 0.1.0. A future release may optionally preserve them in a separate JSON field.

## Condition grades

| Grade | Intended meaning |
| --- | --- |
| `NEW` | New, sealed, or unused |
| `A` | Excellent or like-new |
| `B` | Good, with minor wear |
| `C` | Fair, with visible use |
| `D` | Poor or damaged but identifiable |
| `PARTS` | Junk or parts-only |

Condition terminology is not globally standardized. Users should review the mapping before using grades in contracts or customer quotations.

## Validation

The normalizer reports missing models, invalid quantities and prices, unknown conditions, invalid currency codes, and missing conversion rates. Findings are written to `validation_errors`; rows are retained so operators can correct them without losing source data.

## Currency conversion

Exchange rates are never downloaded automatically. The operator supplies a source-to-target multiplier explicitly, making each conversion reproducible.

Example: JPY 10,000 × `0.0064` = USD 64.00.
