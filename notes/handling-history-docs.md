# Handling history and generated reference (v0.92.0)

Implementation notes for v0.92.0, published October 25, 2026. These notes
record the scoped development decisions; see [release notes](../releases/v0.92.0.md)
for the final publication record.

This replacement extended `handling_events` in place. It did not replace it with
PR #1's `handling_sequence` or rename final-storage summaries. PR #1 was later
closed as superseded without merging its branch.

## Compatible handling history

Existing event keys remain free-text strings or booleans as documented. Their
optional definitions are now explicit under `components`. Two optional additions
are `stage_label` (`initial`, `intermediate`, `final`) and
`storage_degradation_visible` (a list of source-reported free-text observations).

Histories can be partial or empty and have no arbitrary event-count limit. Final
means final known event as of the record, not completed delivery. Labels are
optional; if supplied, initial is first, final is last, and each occurs at most
once. A single event can be labeled final. No initial label is required.

Existing final-storage summaries remain independent. Do not derive or overwrite
them from an incomplete history; preserve disagreements for review. The known
pipe-delimited enum defects remain documented rather than silently migrated.
Omission of damage observations is not proof of inspection or absence of damage.

Legacy event example (unchanged record format):

```yaml
---
handling_events:
  - location_type: farm
    storage_structure: enclosed barn
    duration_estimate: '~1 month'
    restacked: false
```

Partial history with optional annotations:

```yaml
---
handling_events:
  - location_type: dealer yard
    storage_structure: tarp-covered
    duration_estimate: 10-15 days
    restacked: true
    stage_label: final
    storage_degradation_visible:
      - Source reported minor bottom-bale discoloration.
```

These are fragments, not complete hay records. No record migration is required.
Systems may validate supplied stage-label ordering; the structural checker does
not validate hay-record histories.

## Generated documentation

Install `requirements-docs.txt`, then run `python tools/generate_docs.py` and
`mkdocs build --strict`.
The generator writes the overview, one reference page per section, an exact
YAML source copy, and a JSON transcription. Run with `--check` to verify tracked
files are current without writing. Generator output has no timestamps and is
deterministic. It never rewrites the canonical source.

Field lists are traversed in source order. Paths distinguish duplicate identifiers
instead of flattening them into a dictionary. Metadata, enum scalar types, aliases,
and legacy defects remain visible. The overview lists structural warnings and
includes a source hash. The YAML copy retains comments; JSON does not retain YAML
comments and is not JSON Schema. These docs describe the current source tree,
with publication state identified explicitly; generation does not deploy a site.
Every section page carries a visible publication-state notice and links
back to the overview. Source title, version, and status must be strings. Date-like
scalar values must be quoted when intended as strings: the generator rejects
non-JSON YAML values or non-string mapping keys rather than silently converting
their types. Generation errors are detected before output files are written.

All existing fields and summaries are preserved; only `handling_events` gains
optional child definitions and guidance. These changes are included in v0.92.0.
Deployment and broader schema migrations remain separate.
