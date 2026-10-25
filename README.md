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
- [Latest release: v0.92.0](https://github.com/lode-global/hay-spec/releases/tag/v0.92.0)
- [All releases](https://github.com/lode-global/hay-spec/releases)

## Status

- **Source version:** v0.92.0 (published October 25, 2026; specification remains Draft),
  with unreleased optional source-field provenance additions.
- **Latest published:** [v0.92.0](https://github.com/lode-global/hay-spec/releases/tag/v0.92.0)
- **Release notes:** [v0.92.0](./releases/v0.92.0.md)
- **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Maintainer:** [standards@lode.global](mailto:standards@lode.global)

## Release summary: v0.92.0

This minor version adds optional reporting fields, compatibility conventions,
validation tooling, and generated documentation. Existing identifiers and values
remain compatible; the duplicate dry-matter definition is consolidated.
See the [release notes](./releases/v0.92.0.md) for changes, limitations, and
publication details.

## Repository structure

```text
hay-spec/
├── src/                  # Source YAML specification (canonical)
│   └── hay-spec.yaml
├── docs/                 # Generated reference and source transcriptions
├── mkdocs.yml            # Documentation site configuration
├── .github/              # Actions and repo configuration
├── .yamllint             # Lint config
└── .gitignore
```

## Contributing

### Current-source reference documentation

[Browse the generated reference](./docs/index.md). It describes the current
source tree, including unreleased additions; use the tagged releases above for
published snapshots. YAML remains canonical. The generated JSON is a transcription,
not a JSON Schema or a hay-record validator.

Display labels and nutrient-page navigation are maintained in
[`reference-display.yaml`](./reference-display.yaml), separately from the canonical
specification. Labels do not rename record keys; navigation does not regroup stored
fields. Existing source titles take precedence. See the
[display configuration notes](./notes/reference-display.md).

[Try the Traceability field-guide prototype](./docs/guides/traceability.html)
in the locally built site. It provides an expandable outline, searchable labels
and identifiers, field detail cards, and links to the full reference. See
[prototype review notes](./notes/traceability-field-guide.md) for how to preview it.

To regenerate and check the reference locally:

```sh
python -m pip install -r requirements-docs.txt
python tools/generate_docs.py
python tools/generate_docs.py --check
mkdocs build --strict
```

The build creates a local site only. It does not publish or deploy documentation.

To propose changes to the specification, open a GitHub issue or submit a pull request.

See the [carry-forward backlog](./notes/backlog.md) for remaining ideas from the
older draft and the [nutrient compatibility notes](./notes/nutrient-reporting-consistency.md)
for the moisture/dry-matter compatibility decisions.

- 📌 [Contribution Guidelines](./CONTRIBUTING.md)
- 📜 [Code of Conduct](./CODE_OF_CONDUCT.md)

---

_Lode Standards Team_
