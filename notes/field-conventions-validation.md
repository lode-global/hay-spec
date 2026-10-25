# Field conventions and validation (unreleased)

This replacement follows merged PR #4 and recovers the useful conventions from
PR #1 without replacing existing field definitions. PR #1 remains open.

## Interpretation and compatibility

- Prefer `id`; accept legacy `name`, and require equality when both are present.
- Resolve identities within their section and parent, not a global flattened map.
- Keep existing identifiers, enum spellings, data types, nesting, and partial dates.
- Treat titles as labels. No new title or numeric-ID requirement is introduced.
- Distinguish explicit constraints from typical ranges and advisory comments.
- Do not infer mandatory fields, defaults, or values from omissions. Existing
  field/section requirements still apply, including the packaging unit rules.
- Numeric `valid_range` bounds, if used in future changes, are inclusive, finite,
  and permitted only for numeric fields. Conflicting prose is a defect to review,
  not permission to guess precedence.

The machine-readable specification includes these conventions at the top level.
Every existing section and field is unchanged from merged PR #4. In particular,
this PR does not rename `soluble_protein_%_cp` or `degradable_protein_%_cp`.
Their proposed `_pct_cp` replacements need a separately reviewed migration.

## Executable specification checks

Run:

```sh
python tools/validate_spec.py src/hay-spec.yaml --baseline tests/legacy-spec-warnings.json
python -m unittest discover -s tests -v
yamllint -c .yamllint .
```

The checker catches duplicate YAML keys before a parser can overwrite them,
conflicting aliases, malformed field collections, duplicate enum values,
invalid required flags, and inconsistent structured numeric bounds. It reports
legacy naming, enum formatting, and same-scope duplicate identifiers separately.
It does not interpret narrative constraints, check reference registry membership,
or validate hay records, conditional requirements, dates, or scientific content.

CI compares findings to an explicit baseline. New warnings and stale baseline
entries fail the check; errors always fail and cannot be grandfathered. Baseline
paths use list positions, so deliberate field reordering requires baseline review.
Without `--baseline`, warnings are informational and structural errors still fail.

## Existing defects deliberately retained

The baseline records ten findings:

- Two dotted external-lot component identifiers.
- Two protein identifiers containing `%`.
- Five enum lists containing a pipe-delimited string rather than separate values.
- Two `dry_matter` definitions in the same nutrient-analysis field collection
  (one duplicate-identifier finding).

These are preserved to avoid silently changing records or consumer behavior.
Consumers should surface ambiguities instead of selecting a duplicate definition
or automatically splitting stored enum strings. A later migration must specify
how old values map to corrected definitions and how conflicts are handled.

This change adds structure checks, not a complete formal schema or a new release.
Release metadata remains unchanged until maintainers prepare the next release.
