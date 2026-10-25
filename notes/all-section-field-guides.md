# Field guides for every specification section (review prototype)

The guide overview at `/guides/index.html` links all eleven canonical sections
in source order. Newly covered sections are Stand, Location, Soil, Intended use,
Crop management, Harvest, Packaging, Physical characteristics, and Metadata.
Traceability and Nutrient Analysis continue to use the same shared UI.

Install the documentation requirements, run `python tools/generate_docs.py`,
`python tools/generate_docs.py --check`, and `mkdocs build --strict`. Serve `site/`
locally and browse `/guides/index.html`. GitHub displays HTML source rather than
the interactive pages. This change does not deploy a site.

All canonical definitions and metadata are projected without modification.
Component lists (`list` with `item_type: component`) and `object[]` retain their
source types and nesting; their child cards describe members of each entry.
String lists and multi-select enums are labeled distinctly. Source field scope,
identifiers, compatibility aliases, and reference anchors are preserved.
Documentation subsections have no field requiredness badge. Metadata items,
including historical notes and publication text, appear as readable prose rather
than hay-record examples. Historical claims remain as recorded, not reconciled
or certified by the guide.

Definitions, descriptions, details, narration, guidance, source examples, notes,
references, structured bounds, and additional metadata remain available on cards.
Conditional enum/validation guidance is exposed as source metadata. Legacy enum
literal strings containing pipes/backticks remain single literal entries; the UI
never splits or cleans them. Repeated handling history remains independent of
final-storage summaries. Packaging axis/height meaning remains in the existing
source definitions; the guide does not infer dimensions or convert units.

Selected examples and related links are presentation annotations in
`tools/field_guides.py`, not new constraints. They are fragments, not complete
records. Units, requiredness, conditional behavior, and reporting basis remain
as defined by each field. No defaults, calculations, validations, or migrations
are added. The source specification, YAML/JSON downloads, existing reference
pages, publication metadata, and published releases are unchanged.

Review nested Stand and Soil components, Packaging aliases/details, partial-date
and unit guidance, multi-select values, handling-event source examples, legacy
final-storage literals, and Metadata history. Also check source-scoped deep
links, search clearing, keyboard disclosure, and browser Back/Forward.
