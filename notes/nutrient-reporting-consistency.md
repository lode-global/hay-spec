# Nutrient reporting consistency (unreleased)

This proposal follows PRs #4, #5, and #6. PR #1 remains open until the replacement
work has been reviewed. It adds no protein identifier aliases or record migration.

## Moisture and dry matter

`moisture_content` is an optional laboratory-sample water percentage on an
as-received (wet mass) basis. Its inclusive 0-100 range is mathematical, not a
commercial acceptance threshold. No typical 5-45% or similar range is imposed.
Harvest baler moisture remains separate and must not fill a missing lab result.

The two same-scope `dry_matter` definitions become one. The existing identifier,
type, valid-values text, and fuller second definition are retained. No stored hay
record needs a change. The earlier duplicate description is preserved in Git
history; its typical 80-92% range was advisory, not an additional hard constraint.

Only consider complementary results for the same sample and measurement basis.
A missing result may be calculated as 100 minus its complement, with derivation
identified in the implementation's provenance. Do not overwrite a reported value,
invent an unknown value, or impose a universal tolerance on rounded lab reports.
Only emit a calculated value if it satisfies the destination field's existing
constraints; do not clamp results or relax the retained dry-matter constraints.

Examples (fragments, not complete records):

```yaml
---
lab_sample_id: '000123-A'
moisture_content: 12.5
dry_matter: 87.5
```

```yaml
---
dry_matter: 88.0
```

The second record remains valid with no moisture field; absence is not zero.

## Protein identifiers: retained, not renamed

Continue reading and writing `soluble_protein_%_cp` and
`degradable_protein_%_cp`. The proposed `soluble_protein_pct_cp` and
`degradable_protein_pct_cp` names are future candidates, not accepted aliases in
this draft. Introducing them requires an explicit migration decision: which key
is canonical, whether both may be supplied, how disagreement is surfaced, and
which version changes the write format. Never silently normalize incoming keys.
Existing nutrient values, types, typical ranges, and units remain unchanged.

## Validation and release

Compatibility tests compare against merged PR #6 and allow only the optional
moisture definition, removal of the first duplicate, and additional dry-matter
guidance. The legacy warning baseline drops only the resolved duplicate-ID
finding; its nine naming and enum findings remain. Generated docs and their YAML
and JSON copies are regenerated and checked in CI. No release metadata is bumped.
