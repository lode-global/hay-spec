# Contributing to the Hay Description Specification

Thank you for your interest in contributing to the Hay Description Specification.

This project defines a structured, machine-readable format for describing hay and forage products
using YAML. It supports downstream transformations into JSON, Markdown, and other formats and is
intended to serve as an open standard for improved market transparency and analytics.

## Ways to Contribute

- **Propose changes to the YAML schema** (e.g., add, modify, or remove fields)
- **Suggest improvements to definitions, valid values, or field structure**
- **Report issues** with clarity, formatting, consistency, or completeness
- **Share implementation tools** such as validators, converters, or data templates

## How to Submit Changes

1. **Fork the repository** on GitHub
2. Create a feature branch:
   ```bash
   git checkout -b name-of-your-change
   ```
3. Make your edits to `src/hay-spec.yaml`
4. Commit with a descriptive message:
   ```bash
   git commit -m "Refine definition of `leafiness` field"
   ```
5. Push your branch and open a **pull request** (PR) on GitHub

All proposed changes will be reviewed by the maintainers and discussed publicly.

## Style Guidelines

- Use **valid, linted YAML** with consistent indentation
- Match the project’s field structure:
  - `id`
  - `data_type`
  - `valid_values`
  - `definition`
- Use `>` for wrapped multi-line values
- Limit line lengths to ~80–100 characters where possible
- Favor **clarity, conciseness, and neutrality** in definitions

## Getting Help

If you're unsure how to contribute or want feedback on an idea before submitting a pull request,
feel free to [open an issue](https://github.com/lode-global/hay-spec/issues) or contact the
maintainers.

---

This project follows the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md).
