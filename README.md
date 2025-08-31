# hay-spec

**Hay Description Specification**

A structured, machine-readable standard for describing hay and forage products, developed and maintained by the Lode Standards Team.

[![Release](https://img.shields.io/github/v/release/lode-global/hay-spec?display_name=tag&sort=semver)](https://github.com/lode-global/hay-spec/releases)
[![License](https://img.shields.io/badge/license-CC--BY%204.0-blue)](https://creativecommons.org/licenses/by/4.0/)
[![YAML Lint](https://github.com/lode-global/hay-spec/actions/workflows/validate-yaml.yml/badge.svg)](https://github.com/lode-global/hay-spec/actions/workflows/validate-yaml.yml)

---

## Overview

This specification provides a consistent vocabulary and data model for capturing the physical, chemical, and logistical characteristics of hay products. It is designed to support traceability, quality assessment, trade facilitation, and market transparency.

The canonical source of truth is the YAML file in this repository.

- [View the YAML specification](./src/hay-spec.yaml)
- [Latest release: v0.91.1](https://github.com/lode-global/hay-spec/releases/tag/v0.91.1)
- [All releases](https://github.com/lode-global/hay-spec/releases)

## Status

- **Current version:** [v0.91.1 (Draft)](https://github.com/lode-global/hay-spec/releases/tag/v0.91.1)
- **Supersedes:** [v0.91.0](https://github.com/lode-global/hay-spec/releases/tag/v0.91.0)
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Maintainer:** [standards@lode.global](mailto:standards@lode.global)

## Release summary (v0.91.1)

- Corrected top-level metadata: `version: 0.91.1`, `published_on: "2025-08-31"`.
- Added normalized `document_metadata` and human-readable `version_history`.
- YAML validation and style fixes (document start `---`, brace/bracket spacing, indentation).
- No schema changes to fields versus v0.91.0.

## Repository structure

```text
hay-spec/
├── src/                  # Source YAML specification (canonical)
│   └── hay-spec.yaml
├── docs/                 # MkDocs docs (if used)
├── mkdocs.yml            # Documentation site config (if used)
├── .github/              # Actions and repo configuration
├── .yamllint             # Lint config
└── .gitignore
```

## Contributing

To propose changes to the specification, open a GitHub issue or submit a pull request.

- 📌 [Contribution Guidelines](./CONTRIBUTING.md)
- 📜 [Code of Conduct](./CODE_OF_CONDUCT.md)

---

_Lode Standards Team – 2025_
