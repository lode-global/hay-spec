<!-- Generated from notes/legacy-identifier-interoperability.md. -->

# Legacy identifiers: YAML/JSON interoperability examples

These examples demonstrate the current identifiers and nesting. They do not
rename keys, adopt aliases, change definitions or types, or introduce a record
envelope. They are record fragments, not complete records, validation results,
or evidence of nutritional suitability. This is unreleased documentation after
v0.92.0; published assets and canonical source are unchanged.

## External lot identifiers: dots are literal

The existing `lot_identifier_external` component contains two keys whose dots
are part of their names. Preserve the component and those full member names.
Do not flatten them to the root, shorten them to `value` and `issuer`, or expand
the dots into another nested `lot_identifier_external` object.

YAML fragment:

```yaml
---
lot_identifier_external:
  lot_identifier_external.value: '00017-A'
  lot_identifier_external.issuer: USDA
```

Equivalent JSON fragment:

```json
{
  "lot_identifier_external": {
    "lot_identifier_external.value": "00017-A",
    "lot_identifier_external.issuer": "USDA"
  }
}
```

The identifier is an opaque string; preserve its leading zeros, punctuation,
case, and spaces as reported. Do not convert it into a number. `USDA` is an
existing issuer option used only to illustrate structure, not a claim that an
authority issued this example identifier.

Download the matching [YAML fragment](../examples/legacy-identifiers/external-lot.yaml)
and [JSON fragment](../examples/legacy-identifiers/external-lot.json).

## Protein identifiers: percent signs are literal

Retain `soluble_protein_%_cp` and `degradable_protein_%_cp` exactly. The percent
sign is part of each key. These existing fields remain scalar measurements,
not nested nutrient objects. Quoting keys in YAML makes their spelling explicit;
quotes are syntax, not part of the stored identifier.

YAML fragment:

```yaml
---
"soluble_protein_%_cp": 25.0
"degradable_protein_%_cp": 65.0
```

Equivalent JSON fragment:

```json
{
  "soluble_protein_%_cp": 25.0,
  "degradable_protein_%_cp": 65.0
}
```

The values illustrate numeric scalars only. Read each canonical definition for
reporting basis and meaning. This example does not convert values, establish a
hard range, infer other measurements, or prescribe a laboratory result.
Do not substitute `_pct_cp` names or write both spellings as if an alias policy
already existed. No such migration or conflict-precedence rule is adopted here.

Download the matching [YAML fragment](../examples/legacy-identifiers/protein.yaml)
and [JSON fragment](../examples/legacy-identifiers/protein.json).

## Documentation locations are not record keys

A documentation location such as
`traceability/lot_identifier_external/lot_identifier_external.value` identifies a
field within the reference. `traceability` is a documentation section, not a new
record container. The slashes separate documentation ancestors; the dot in the
last segment remains literal. Similarly,
`nutrient_analysis/soluble_protein_%_cp` does not add a `nutrient_analysis` wrapper
to these fragments. Guides may URL-encode characters in navigation links; that
does not encode or rename the stored keys.

Use object-key access that treats names literally. Libraries that interpret
periods as paths need escaping or a literal-key API; do not pass these identifiers
to a path-expanding setter without checking its behavior.

## What the round-trip checks establish

The downloadable YAML and JSON pairs parse to the same mappings. Tests reserialize
and parse them again in both directions and check exact keys, nesting, string
identifiers, and numeric scalar types for these fixtures. They do not promise
byte-identical formatting, comments, quote style, ordering, floating-point lexical
precision, or support for arbitrary YAML-specific types in JSON. They are not a
general record converter, JSON Schema, or hay-record validator. The repository's
specification JSON download is a separate transcription of the specification,
not one of these example records.

## Decisions still open

Renaming the protein keys or adding aliases for dotted identifiers still requires
a separate versioned proposal defining old/new coexistence, conflicts, read/write
behavior, and lossless preservation of historical records. These examples make
current implementations clearer without deciding that migration.
