<!-- Generated from notes/legacy-storage-enums.md. -->

# Legacy storage enums: interpretation and compatibility

This guide explains retained source wording; it does not correct allowed values,
change types, authorize a migration, or introduce new record structures. Canonical
YAML remains authoritative. This is unreleased documentation after v0.92.0;
published assets and existing definitions are unchanged.

## What the source actually contains

Each affected field is declared as `data_type: enum`. Each `valid_values` list
contains **one string with literal pipe characters**, not several YAML entries:

| Field in Physical Characteristics and Condition | Sole parsed `valid_values` entry |
| --- | --- |
| `final_storage_structure` | <code>field &#124; tarp-covered &#124; open shed &#124; enclosed barn &#124; unknown</code> |
| `final_surface_type` | <code>ground &#124; pallets &#124; wood &#124; concrete &#124; other</code> |
| `final_airflow_condition` | <code>natural ventilation &#124; forced ventilation &#124; enclosed with limited airflow &#124; unknown</code> |
| `restacked_since_baling` | <code>true &#124; false &#124; unknown</code> |
| `visible_moisture_damage` | <code>true &#124; false &#124; unknown</code> |

For example, the retained YAML declaration:

```yaml
valid_values: [true | false | unknown]
```

parses as a one-element sequence containing the string `true | false | unknown`.
The words `true` and `false` inside that string are not YAML booleans. This is a
specification-definition fragment, not a hay-record example.

Some definition prose describes individual choices, particularly for storage
structure. That prose and the parsed list do not establish one unambiguous,
interoperable choice set. The current source has not been migrated to separate
entries. The structural checker reports these five declarations as acknowledged
`legacy_enum_literal` warnings; it does not validate hay records.

## Preserve reported values

Do not split a stored pipe-containing string into a list, tokenize it into
several selections, or choose a token automatically. Do not replace the enum
with a boolean field or convert reported strings `"true"` and `"false"` into
boolean values. Do not trim, change case, or rewrite a reported value to make it
match an application's preferred options.

Preserve the original reported value and scalar type, including unfamiliar or
conflicting reports. Retention for review is not a declaration that a report
conforms. This guide neither adds individual tokens to canonical allowed values
nor requires consumers to accept every input as valid. Consumers should explain
their own interpretation and acceptance rules separately from the specification.
New-entry interfaces should disclose the unresolved source limitation rather
than advertise a corrected choice set as canonical. Any application-specific
choices or mappings must remain explicit and must not overwrite the original.

For example, a reported string `"true"` and a reported boolean `true` remain
distinct reports. Neither is declared conforming by this guide. A reported string
`"ground | pallets | wood | concrete | other"` is not five reported surfaces.
These are preservation scenarios, not newly approved hay-record examples.

## Relationship to handling history

Keep these summaries independent of `handling_events`. Its free-text
`storage_structure`, `surface_type`, and `airflow_condition` components do not
repair the summary enums. Do not copy, infer, overwrite, or synthesize summaries
from a partial handling history. If summaries and events disagree, preserve both
and flag the discrepancy for review. This guidance retains the existing handling
history rules and does not add a second record layout.

## Decisions required before a correction

A separate versioned proposal should determine:

- The intended allowed values, including exact spelling and scalar types. Decide
  explicitly whether boolean-looking choices are strings or booleans; define the
  meaning of omission, `unknown`, and `other` for each field without inventing
  defaults for old records.
- Read and write behavior for historical full pipe strings, individual tokens,
  booleans, unfamiliar values, and ambiguous or conflicting inputs. Historical
  data may vary; do not assume one representation was universally used.
- Whether corrected choices use the same fields or a new representation; define
  precedence and conflict handling if old and new forms coexist.
- Explicit mappings, source-value retention, review of lossy or ambiguous cases,
  and whether reversal is possible. Do not infer a unique choice from a pipe
  string or manufacture missing information.
- Release/version policy, consumer capability expectations, examples, and
  compatibility tests before changing allowed values or stored records.

No correction or migration is selected here. Identifier changes, numeric IDs,
reference registries, and new handling fields remain outside this guidance.
