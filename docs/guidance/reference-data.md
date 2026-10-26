<!-- Generated from notes/reference-data-policy.md. -->

# Reference data for forage varieties and testing laboratories

This is implementation guidance and a proposal gate for future datasets, not a
new enum list, registry, record format, or migration. Canonical YAML definitions
remain authoritative. No dataset is adopted, required, or certified by this PR.
Published v0.92.0 assets and existing records are unchanged.

## Current limitations

`stand/forage_variety_components/forage_variety` is an enum whose `valid_values`
contains the descriptive placeholder “reference list of forage species,
subspecies, or named varieties”. It does not identify a downloadable list,
version, or globally stable identifier scheme. Species, cultivar, and commercial
names must not be assumed to be interchangeable.

`nutrient_analysis/hay_testing_laboratory` is an enum with the retained values
`list of recognized lab names` and `Internal lab`. The first is unresolved
reference-list wording, not an adopted directory. `Internal lab` remains an
existing literal. The source discusses recognized laboratories and proficiency
programs, but this repository does not supply an authoritative list or establish
a laboratory's certification, accreditation, or current proficiency status.

These limitations do not turn either enum into an unrestricted string field.
They also do not justify rejecting historical records solely because an optional
lookup cannot resolve their reported value. Consumers should disclose their
application's acceptance rules separately from canonical specification rules.

## Optional lookup behavior

Lookup assistance may suggest display labels or candidate matches. Preserve the
original stored value, spelling, punctuation, case, and structure. Do not replace
a reported variety or laboratory with a registry ID, a corrected name, `other`,
`unknown`, or `Internal lab`. No new fallback literal or comments field is added
here. Do not merge similar names automatically or infer species, GMO status,
certification, accreditation, testing method, or feeding suitability from a match.

If a lookup is unavailable, ambiguous, or has no match, retain the record and
show that lookup status separately in the application. This is not a declaration
that the record passes all validation. New-entry acceptance remains an explicit
consumer policy; this guidance does not expand the canonical allowed values.

For illustration, the source's `Tifton 85 bermudagrass` wording may be shown
alongside candidate catalogue entries without changing the stored text. A report
using `Internal lab` retains that exact value even if the application also knows
the organization's name. An unfamiliar historical laboratory name remains
available for review; a failed search alone does not establish invalidity.
These are lookup scenarios, not complete records or newly approved enum values.

Any consumer-maintained match metadata should remain outside the canonical hay
record for now. Record the catalogue, its version, candidate identifier, and
review decision in the consumer's own system if needed; these are not new
specification fields. An explicit future extension would be needed to standardize
such metadata in exchanged records.

## Requirements before adopting a dataset

A separately reviewed proposal should establish:

- **Ownership and scope:** accountable maintainer, geographic and language
  coverage, inclusion criteria, correction process, and maintenance commitment.
  Distinguish botanical taxa, named cultivars, and commercial products; distinguish
  laboratory organizations, sites, and names used on reports.
- **Rights:** provenance, reuse and redistribution licence, attribution, and
  permission to distribute any pinned snapshot with documentation or software.
- **Identity:** dataset namespace, stable opaque identifiers, alias policy, and
  treatment of renames, mergers, splits, duplicates, and retired entries. Never
  reuse an identifier for a different entity or equate names across catalogues.
- **Versioning:** immutable versioned snapshots, change notes, retrieval location,
  integrity information, and reproducible historical lookup. A changing “latest”
  endpoint alone is insufficient for interpreting old records.
- **Availability:** offline/cache behavior, outage and withdrawal handling,
  update policy, and support for unavailable, unmatched, or ambiguous entries.
  Historical values must remain readable without a live registry dependency.
- **Compatibility:** optional adoption, exact preservation of existing values,
  explicit mapping review, and rules for conflicting old/new representations
  before any identifier field or allowed-value change is proposed.
- **Claims:** distinguish catalogue membership from verified identity and from
  time-sensitive accreditation, proficiency participation, or certification.
  Such claims require their own evidence, scope, and dates.

## Decisions still open

No preferred catalogue or registry is selected. Maintainers must still decide
who will own each dataset, which regions and entity types it covers, whether
redistribution is permitted, how snapshots will be hosted, and whether lookup
will remain consumer-side or merit a later optional exchange extension. Any
canonical change needs its own compatibility review and release decision.
