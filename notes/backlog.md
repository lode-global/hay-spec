# Hay specification carry-forward backlog

Recorded after replacing the principal work in PR #1 through PRs #4, #5, and #6.
These are ideas for separately reviewed changes, not accepted field definitions
or authorization to migrate records. PR #1 remains open pending replacement review.

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
- Optional display titles and nutrient grouping for documentation and forms,
  without restructuring records or requiring numeric IDs. Numeric IDs need a
  specific stable-identity use case and allocation policy before adoption.
- Forage-variety and laboratory reference datasets: define ownership, versioning,
  identifier policy, availability, and fallback behavior before requiring them.
- Consider glyphosate-specific production disclosure only after a separate domain
  review of need, terminology, overlapping categories, and relationship to existing
  herbicide fields. Do not infer compliance or feeding suitability from disclosure.

## Maintenance and release

- Reconcile historical version-history claims with actual field definitions.
- Select the next release number and update publication metadata and release notes
  together; generated current-source docs do not themselves publish a release.
- Decide whether and where to deploy the documentation site.
- Once replacement review is complete, close PR #1 as superseded with links to the
  replacement PRs and this backlog. Retain its history; do not merge the old branch.

Do not carry forward the old draft's arbitrary nutrient limits, unreviewed type
changes, mandatory unavailable registries, older lint configuration, or replacement
of `handling_events` with `handling_sequence`.
