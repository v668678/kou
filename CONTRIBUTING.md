# Contributing

Contributions that improve real inventory workflows are welcome.

## Useful contributions

- Header aliases used by Japanese, Chinese, or English suppliers.
- Condition-grade mappings with a clear explanation of the source convention.
- Reproducible bug reports with anonymized sample rows.
- Tests for unusual CSV encodings, numeric formats, and identifier formats.
- Documentation improvements and translations.

Do not submit real customer names, complete IMEI values, serial numbers, addresses, or confidential pricing.

## Development

```bash
python -m unittest discover -s tests -v
```

Keep changes focused and add tests for behavior changes. Open an issue before large schema changes so downstream compatibility can be discussed.
