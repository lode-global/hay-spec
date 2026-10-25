# Nutrient Analysis field guide (review prototype)

The guide at `guides/nutrient_analysis.html` shares the Traceability guide's
outline, search, field cards, breadcrumbs, deep links, and Back/Forward behavior.
It uses the ten ordered groups in `reference-display.yaml`. Groups are visual
navigation aids, not record objects: all 70 canonical direct source nodes,
including documentation markers, retain their identifiers, order, and anchors.
The existing percent-bearing protein keys are literal and remain unchanged.

Groups initially collapse to keep the outline manageable. Searching expands
matching paths; a direct field deep link expands its group. Clearing search keeps
the selected field's group expanded, so the outline stays consistent with its card. Documentation-marker
cards are explicitly labeled as having no stored value. Group cards have no
record identifier and link to the corresponding reference navigation anchor.

Cards show the full source definition, guidance, value guidance/enumerations,
structured numeric bounds, notes, references, and other source metadata where
present. Units and reporting basis remain as stated by each field: there is no
inferred common basis, unit conversion, complementary-value calculation, or new
validation rule. Typical ranges in prose remain advisory. Optionality is only
shown when explicit in the source; other value fields direct readers to their
definition. Examples are illustrative fragments, not feeding recommendations.
Read-alongside links connect selected provenance and reporting concepts without
asserting automatic dependencies or derived values.

Run the existing documentation generation/check commands and strict site build.
Serve `site/` locally and open `/guides/nutrient_analysis.html`. Review sampling,
moisture/dry matter, protein fractions, energy units, and minerals; try exact-ID
search, percent-bearing deep links, keyboard disclosures, and Back/Forward.
The page works without external scripts or runtime dependencies; without
JavaScript it links to the complete reference. No deployment is included.

Canonical YAML, generated source YAML/JSON, existing record structures, and
publication metadata are unchanged. The v0.92.0 release remains unchanged.
