# Hay specification carry-forward backlog

Recorded after replacing the useful work in [PR #1](https://github.com/lode-global/hay-spec/pull/1)
through merged [PR #4](https://github.com/lode-global/hay-spec/pull/4),
[PR #5](https://github.com/lode-global/hay-spec/pull/5),
[PR #6](https://github.com/lode-global/hay-spec/pull/6), and
[PR #7](https://github.com/lode-global/hay-spec/pull/7).
These are ideas for separately reviewed changes, not accepted field definitions
or authorization to migrate records. Replacement review is complete; PR #1 is
superseded. Its remaining useful ideas are recorded below. Do not merge the old branch.

## Compatibility migrations

- Decide a versioned migration for the two protein identifiers containing `%`.
  Preserve original keys and define handling of simultaneous old/new keys and
  conflicting values before adopting `_pct_cp` names.
- Resolve the five pipe-delimited enum lists without silently splitting stored
  strings. Document read/write behavior and conversion of historical records.
- Decide whether dotted external-lot component identifiers should remain or gain
  explicitly documented aliases; never flatten nested identifiers automatically.

## Useful additions

- Optional source-field name and identifier for traceability. Define identifier
  scope/issuer and multiple-field representation; avoid the old draft's conflicting
  `multi_field` and `multi-field` sentinels.
- Display titles and nutrient-reference navigation are implemented in the
  presentation configuration; see [configuration notes](reference-display.md).
  Form integration remains a consumer decision. Numeric IDs still need a specific
  stable-identity use case and allocation policy before adoption.
- Forage-variety and laboratory reference datasets: define ownership, versioning,
  identifier policy, availability, and fallback behavior before requiring them.
- Consider glyphosate-specific production disclosure only after a separate domain
  review of need, terminology, overlapping categories, and relationship to existing
  herbicide fields. Do not infer compliance or feeding suitability from disclosure.

## Maintenance and release

- Reconcile historical version-history claims with actual field definitions.
- v0.92.0 records the completed publication preparation. For future releases,
  update version, publication metadata, release notes, and generated docs together.
- Decide whether and where to deploy the documentation site.
- Preserve PR #1 as historical context for the merged replacements and this backlog;
  future work should start from current main rather than merge the old branch.

Do not carry forward the old draft's arbitrary nutrient limits, unreviewed type
changes, mandatory unavailable registries, older lint configuration, or replacement
of `handling_events` with `handling_sequence`.
