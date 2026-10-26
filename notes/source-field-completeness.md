# Optional source-field list completeness (unreleased)

`source_fields_completeness` is an optional enum beside `source_fields` in
Traceability. Existing field definitions and record structures remain unchanged.
Existing records need no migration. Consumers that accept enriched records must
tolerate this new optional field. This is unreleased work after v0.92.0; published
assets, version metadata, and original historical notes are unchanged.

## Meaning and limits

- `complete`: the source asserts that every production field contributing to the
  hay described by this record is represented in `source_fields`.
- `partial`: the source asserts that at least one contributing production field
  is omitted from the supplied list.
- Omission: no completeness assertion. It does not imply either value, unknown
  origin, or single-field production. There is no `unknown` sentinel or default.

Both supplied values expect a nonempty list. The scope is the hay represented by
this record, not the entire farm's inventory or all fields used in a season.
Completeness is source-reported list coverage, not independently verified origin,
identity uniqueness, allocation of mass or percentages, or bale-level mapping.
Do not derive it from list length, lot flags, or names and identifiers. Preserve
all existing `source_fields` entry rules and identifiers exactly as reported.

If the list or represented hay changes, reassess the assertion. Do not copy it
automatically into a blend, split, or new lot. This addition does not change lot
identifiers, `hay_single_lot_traceable`, mapping capability, or location summaries.

## Examples

These are Traceability fragments, not complete records or validation results.

Existing record without an assertion (unchanged meaning):

```yaml
---
source_fields:
  - field_name: North meadow
```

Complete list for hay contributed by one field:

```yaml
---
source_fields:
  - field_name: North meadow
source_fields_completeness: complete
```

Complete list for hay contributed by multiple fields:

```yaml
---
source_fields:
  - field_identifier: '001-A'
    field_identifier_scope: Example Farm / field register
  - field_name: South meadow
source_fields_completeness: complete
```

Partial list (other contributing fields are omitted):

```yaml
---
source_fields:
  - field_name: North meadow
source_fields_completeness: partial
```

Conflicting report retained for review, not a conforming example:

```yaml
---
source_fields: []
source_fields_completeness: complete
```

## Inconsistencies and implementation guidance

An assertion with an omitted or empty `source_fields` list is inconsistent.
Retain the reported values and flag the conflict for review; do not erase the
assertion, invent a field, infer a value, or silently normalize the report.
`null`, blank strings, and values other than `complete` and `partial` are not
accepted declarations. Retaining a report for review does not make it conforming.

The repository's structural checker validates specification definitions, not
hay records. The examples and tests demonstrate the contract; this PR does not
add a general-purpose record validator or alter acceptance of historical records.
