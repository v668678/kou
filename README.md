# Reuse Trade Toolkit

Open-source utilities for cleaning and standardizing second-hand electronics inventory before cross-border trade, quotation, and internal analysis.

The project focuses on a common operational problem: inventory files arrive with mixed Japanese, Chinese, and English headers, inconsistent condition grades, different currencies, and sensitive device identifiers.

## Features

- Normalize Japanese, Chinese, and English CSV headers into one schema.
- Standardize product categories and condition grades.
- Convert unit prices with an explicitly supplied exchange rate.
- Mask IMEI and serial numbers while retaining the last four characters.
- Report row-level validation errors instead of silently discarding data.
- Produce a compact inventory summary for procurement review.
- Run entirely with the Python standard library.

## Quick start

Python 3.10 or newer is recommended.

```bash
python -m reuse_trade_toolkit normalize \
  examples/inventory_ja.csv normalized.csv \
  --target-currency USD \
  --rate 0.0064 \
  --mask-identifiers
```

Generate a summary:

```bash
python -m reuse_trade_toolkit summarize normalized.csv
```

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

## Normalized schema

| Field | Description |
| --- | --- |
| `item_id` | Supplier or internal inventory identifier |
| `category` | `smartphone`, `tablet`, `component`, `vehicle`, or `other` |
| `brand` | Manufacturer or brand |
| `model` | Product or vehicle model |
| `condition` | `NEW`, `A`, `B`, `C`, `D`, or `PARTS` |
| `quantity` | Positive integer quantity |
| `unit_price` | Decimal unit price |
| `currency` | Three-letter currency code |
| `serial_number` | Optional serial number |
| `imei` | Optional IMEI |
| `notes` | Free-text notes |
| `validation_errors` | Pipe-separated validation findings |

See [docs/schema.md](docs/schema.md) for mappings and validation rules.

## Privacy

Device identifiers can be sensitive. Use `--mask-identifiers` before sharing files with buyers, logistics providers, or external analysis systems. This tool does not upload inventory data or call any external service.

## Project scope

The initial release concentrates on deterministic inventory preparation. Planned work includes configurable mappings, HS-code assistance, duplicate detection, and reusable procurement-quality reports.

The repository also hosts the SANYOU Company website in `index.html`, providing operational context for the reuse and recycling workflows that motivated the toolkit.

## Contributing

Bug reports, sample schemas, translations, and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT License. See [LICENSE](LICENSE).
