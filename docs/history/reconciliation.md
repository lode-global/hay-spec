<!-- Generated from notes/version-history-reconciliation.md. -->

# Reconciled version history

This audit corrects interpretation of the retained historical notes; it does not
change any field definition, identifier, value, type, constraint, or record
structure. It is unreleased documentation work after v0.92.0. Published tags and
release assets are not rewritten.

## Original notes and scope

The [verbatim archive](archive/version-history-original.txt) contains the complete
`version_history` subsection, including its original indentation and wording,
extracted from [pre-audit main, commit 31614e5](https://github.com/lode-global/hay-spec/blob/31614e5d3a289499d7d7648709d457edf94f7a81/src/hay-spec.yaml).
Its SHA-256 is
`b75a38df6a191cded357768abb126443abb0d96ec8710ea899487d5a6f78e072`.
The same historical subsection remains unchanged in canonical YAML. Read its
claims alongside this audit, rather than as a verified inventory or migration
instruction. This report is the reconciled interpretation, not a new release.

Evidence consists of repository tag targets, exact tagged `src/hay-spec.yaml`
bytes, parsed field definitions where parsing succeeds, and introducing commits.
Commit dates, dates inside documents, and actual publication timestamps are
separate facts. This audit does not establish GitHub publication times or verify
external scientific/reference claims.

## Tagged snapshots

| Tag | Resolved commit | What can be verified |
| --- | --- | --- |
| [v0.90.0 source](https://github.com/lode-global/hay-spec/blob/v0.90.0/src/hay-spec.yaml) | `98fce9dd1c763ab824557b036b7a4c645b71e192` | Parses as YAML. Initial-draft history records May 5, 2025; the tag target commit is also dated May 5. This is not a proof of publication time. |
| [v0.91.0 source](https://github.com/lode-global/hay-spec/blob/v0.91.0/src/hay-spec.yaml) | `b10ecc7798926355804abd226d001d77305f502c` | Contains refactor text but fails whole-document YAML parsing. PyYAML reports an unexpected root-level `- id: metadata` at line 7671. Do not repair it silently and call the result the published schema. |
| [v0.91.1 source](https://github.com/lode-global/hay-spec/blob/v0.91.1/src/hay-spec.yaml) | `486d175740d3ecc5be583b3da601170081d14049` | Parses as YAML. All ten non-metadata sections are equal to v0.90.0 after parsing. Metadata includes version 0.91.1 and quoted `published_on: 2025-08-31`. |
| [v0.92.0 source](https://github.com/lode-global/hay-spec/blob/v0.92.0/src/hay-spec.yaml) | `37556a56e59f82db9618b29245614b57d4a1c5ad` | Parses as YAML and includes the reviewed compatible additions described below. Its published metadata records October 25, 2026; the specification remains draft. |

The v0.91.0 header records `date_published: 20250809`, whereas its target
commit is dated August 31 and the retained history also labels August 31. These
conflicting recorded dates are not resolved into a publication timestamp here.

The v0.91.0 and v0.91.1 tag targets are on divergent histories with common
ancestor `a70cc88ca0de37b6be58589866661c0f2dd5c0d0`. Neither tag target is an ancestor
of the other. Do not describe v0.91.1 as merely an in-place formatting patch to
the v0.91.0 tagged file, or infer an automatic record migration between them.

## Audit of the original claims

"Text present" below means only that the malformed v0.91.0 file contains that
text; it does not establish a usable parsed model or a change retained later.

| Original claim | Finding and corrected interpretation |
| --- | --- |
| v0.90.0 initial draft dated May 5, 2025 | Supported as a recorded document date and tag-target commit date. Public launch timing and stakeholder history are outside this audit. |
| v0.91.0 began a DRY refactor and clarified groups/naming | Refactor text is present, including nested groups and naming policy. Whole-document validity is not established: the tagged file fails parsing. Do not use this prose to reinterpret v0.91.1 records. |
| v0.91.0 enforced ASCII-only content and unit/encoding policies | The tagged text declares policies; that is not evidence of enforcement by implementations. v0.91.1 contains non-ASCII history punctuation. No normalization or unit conversion is authorized. |
| v0.91.0 introduced version history and document metadata conventions | Version history already exists in v0.90.0. The v0.91.0 text adds/expands metadata conventions, but "introduced" is too broad. |
| v0.91.0 replaced fertilizer inputs with `fertilizer_application` | That identifier appears in v0.91.0 text. v0.91.1 and current main retain separate fertilizer dates, amounts, and units; the refactor must not be inferred for those records. |
| v0.91.0 refactored organic amendments to object arrays | v0.91.0 text contains `organic_amendments`; v0.90.0 and v0.91.1 already have `organic_amendments_applied` with `data_type: list`, `item_type: component`. Preserve that actual identifier and structure. |
| v0.91.0 reworked stand composition | Refactor text is present, but v0.91.1's complete Stand section equals v0.90.0's. Do not attribute a retained stand-field migration to v0.91.1. |
| v0.91.0 converted harvest start/end to datetime | Both fields already have `data_type: datetime` in v0.90.0 and retain it in v0.91.1. It is not a newly retained type change in that line. |
| v0.91.0 began dual dry-matter/as-fed nutrient objects | Such reporting text appears in v0.91.0. v0.91.1 retains scalar nutrient definitions; current main does not gain dual-reporting objects from a historical note. |
| v0.91.0 added laboratory processing/provenance fields | `lab_sample_id` and related text appear in v0.91.0, but the fields are absent from v0.91.1. The compatible fields retained on current main were introduced by the later reviewed packaging/laboratory work included in v0.92.0. |
| v0.91.0 standardized `valid_range` and `enum_select_mode` | Those keys appear in the malformed tag. They do not establish constraints on v0.91.1 or current records. Current structured conventions and the laboratory-moisture bounds came through later reviewed changes. |
| v0.91.1 corrected publication metadata and YAML style | Metadata corrections are visible. However, the original "no schema changes compared to v0.91.0" claim is unsupported: the tag targets diverge and v0.91.0 does not parse. The verified equality is v0.91.1 versus v0.90.0 for the ten non-metadata sections. |
| v0.92.0 compatible reporting/documentation improvements | Supported by the tagged snapshot and introducing commits below. This does not incorporate the old refactor wholesale, rename protein keys, repair legacy enum literals, or change handling-history keys. |

## Verified v0.92.0 changes

- [Packaging and laboratory provenance, PR #4](https://github.com/lode-global/hay-spec/pull/4):
  commit `3a6a5b7` adds packaging `id` aliases, a round-bale axis field, and five
  optional laboratory provenance fields. Commit `dceef33` preserves ambiguous
  legacy round-bale height measurements rather than reinterpreting them.
- [Field conventions and validation, PR #5](https://github.com/lode-global/hay-spec/pull/5):
  commit `b79cb2b` adds interpretation conventions and structural checks. These
  validate specification structure, not hay records or scientific suitability.
- [Handling history and reference generation, PR #6](https://github.com/lode-global/hay-spec/pull/6):
  commit `50e9032` adds optional definitions/guidance within `handling_events`
  and generated documentation; it does not replace the existing record key.
- [Nutrient consistency, PR #7](https://github.com/lode-global/hay-spec/pull/7):
  commit `507bd65` adds optional laboratory moisture and consolidates the duplicate
  `dry_matter` definition without renaming its record key.
- [Release preparation, PR #8](https://github.com/lode-global/hay-spec/pull/8),
  followed by publication-finalization commit `37556a5`, records v0.92.0 metadata
  and generated sources. See the immutable
  [v0.92.0 release notes](https://github.com/lode-global/hay-spec/blob/v0.92.0/releases/v0.92.0.md).

## Changes after v0.92.0: merged, unreleased

- [PR #9](https://github.com/lode-global/hay-spec/pull/9), commit `52377fa`:
  presentation-only display titles and nutrient navigation.
- [PR #10](https://github.com/lode-global/hay-spec/pull/10), commit `8ef6760`:
  optional `source_fields` provenance for one or multiple contributing fields.
- [PR #11](https://github.com/lode-global/hay-spec/pull/11), commit `8cacb2a`:
  Traceability field-guide prototype.
- [PR #12](https://github.com/lode-global/hay-spec/pull/12), commit `35cd997`:
  Nutrient Analysis guide.
- [PR #13](https://github.com/lode-global/hay-spec/pull/13), commit `31614e5`:
  remaining section guides and a guide overview.

These changes are not retrospectively part of the v0.92.0 tag. This audit does
not assign them a future release number, tag them, or publish them.
