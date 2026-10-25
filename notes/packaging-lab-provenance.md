# Packaging and laboratory provenance (unreleased)

This proposal recovers a limited part of PR #1 on top of current main. It does
not merge that branch, change the release version, or close PR #1.

## Compatibility and packaging

All twelve existing packaging fields already exist in v0.91.1 under `name`.
They now also expose matching `id` keys, consistent with other sections.
The `name` aliases and existing enum values remain unchanged. Consumers should
prefer `id`, falling back to `name` when reading older specifications. A consumer
must treat matching `id` and `name` as one field, not two fields.

Weight units cover intended harvest weight, average weight, and intended
repackaged weight. Dimension units consistently permit inches, centimeters,
feet, and meters. Measurements must be positive and finite; typical bale sizes
are not hard limits. Units are required when their measurements are supplied.
Omission means not reported, not zero.

Rectangular dimensions retain the released orientation-based conventions.
Round bales gain `bale_dimension_axis`. Prefer diameter and axis for new round
bale records. Legacy round width means diameter and legacy round height means
axis length. When both old and new measurements are provided, they must agree
after conversion. Do not silently reinterpret old records as sorted dimensions.

Examples (record fragments, not complete hay records):

```yaml
---
bale_shape: rectangular
bale_dimension_width: 3
bale_dimension_height: 4
bale_dimension_length: 8
bale_dimension_units: feet
average_bale_weight: 1200
bale_weight_units: pounds
```

```yaml
---
bale_shape: round
bale_dimension_diameter: 150
bale_dimension_axis: 120
bale_dimension_units: centimeters
average_bale_weight: 500
bale_weight_units: kilograms
```

## Laboratory provenance

Five optional fields are added: `lab_sample_id`, `lab_report_reference`,
`lab_processing_completed_date`, `lab_processing_notes`, and `lab_quality_code`.
Sample IDs and quality codes are scoped to the reporting laboratory; they are
not global identifiers or standardized hay grades. Report references may be
identifiers, filenames, or URIs and do not imply public access.

The processing date means sample preparation, not collection or analysis. It
uses the existing YYYYMMDD/partial-date convention rather than introducing a
new date format. Missing provenance does not invalidate a historical test.

```yaml
---
hay_tested: true
hay_testing_laboratory: Internal lab
hay_sample_date: '20261001'
lab_sample_id: '000123-A'
lab_report_reference: 'report-000123-A.pdf'
lab_processing_completed_date: '20261002'
hay_testing_date: '20261003'
lab_processing_notes: Sample reground before analysis.
lab_quality_code: R
```

No laboratory registry requirement, nutrient ranges, nutrient data types,
handling-history replacement, enum renaming, numeric IDs, or general field
metadata refactor is included. Existing laboratory selection behavior is kept.

## Validation and remaining review

Run `python3 -m unittest discover -s tests -v` with PyYAML installed, followed by
`yamllint -c .yamllint .`. The focused tests protect the specification contract;
they are not a general hay-record validator. YAML lint establishes formatting
and syntax, not scientific validity.

Before release, maintainers should confirm the legacy round-height interpretation
with any existing implementations and choose the release number. Keep v0.91.1
metadata unchanged until that release is prepared.
