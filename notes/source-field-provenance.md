# Optional source-field provenance (unreleased)

`source_fields` is an optional `object[]` in traceability. Existing records remain
valid unchanged. It supplies references to contributing production fields, not a
replacement for lot identifiers or existing location and traceability summaries.
Older consumers must tolerate unknown optional fields to accept enriched records.

Use one entry per field. Each entry must provide a nonblank `field_name` or
`field_identifier`; `field_identifier_scope` alone is insufficient. All supplied
values are strings. Individual components are optional so a name-only reference
or a source identifier without known scope can be retained. Preserve opaque
identifiers exactly; do not convert numbers, trim punctuation, or merge references
using names or unscoped identifiers. Supply issuer/namespace context where known.

Omission and an empty list both supply no details; neither means single-field,
unknown origin, or complete coverage. No sentinel value or registry is needed.
The list can be partial and has no arbitrary count limit. Order conveys no
priority or contribution share. Do not derive lot flags, mapping capability,
location summaries, or single-lot status from list length. Inconsistent reports
remain available for review. Quantities, coverage assertions, and bale-to-field
relationships are outside this addition.

These are traceability fragments, not complete hay records.

Existing record (no migration):

```yaml
---
lot_identifier_internal: LOT-042
hay_single_lot_traceable: true
```

Single field, identified by name alone:

```yaml
---
source_fields:
  - field_name: North meadow
```

Multiple fields; the same identifier can occur in distinct scopes:

```yaml
---
source_fields:
  - field_name: North meadow
    field_identifier: '001-A'
    field_identifier_scope: Example Farm / field register
  - field_identifier: '001-A'
    field_identifier_scope: Neighbor Farm / field register
```

No details supplied:

```yaml
---
source_fields: []
```

The structural checker validates specification definitions, not hay records.
The entry-content rules above are guidance for record implementations; tests check
these examples and compatibility, not a general-purpose record validator.

This is unreleased work after v0.92.0. The version and publication dates retained
in source metadata describe the last release; `publication_status: unreleased`
and the generated current-source notice distinguish the working tree. Published
v0.92.0 assets are unchanged. No new release or tag is prepared by this change.
