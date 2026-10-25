# Traceability field-guide prototype

This read-only prototype offers an expandable outline and selected-field cards,
with name/identifier search, documentation breadcrumbs, source definitions,
declared values, examples, related-field links, and links to full reference anchors.
Native disclosures and buttons support keyboard navigation. At narrow widths the
outline stacks above the detail card. No record editing, submission, analytics,
external scripts, fonts, or network requests are added.

Run `python tools/generate_docs.py`, `python tools/generate_docs.py --check`, and
`mkdocs build --strict`. Then run `python -m http.server --directory site 8000`
and open `http://localhost:8000/guides/traceability.html`. The documentation menu
also links to the guide. GitHub's file view shows HTML source rather than a live
preview. No documentation deployment is part of this change.

The guide uses canonical definitions and the display overlay. Examples and
related-field links are presentation annotations in `tools/traceability_guide.py`;
the UI template is `tools/templates/traceability-guide.html`. Generated HTML is
tracked under `docs/guides/traceability.html` and checked by the existing freshness
command. The prototype does not interpret the specification as JSON Schema.

Sections are documentation organization, components are structured blocks, and
object arrays are repeated entries. Dotted member identifiers remain literal.
The guide does not introduce a section envelope or change record nesting. Fields
without an explicit `required` value say to consult the definition; the guide
does not infer new mandatory/optional rules. Source-field entry rules are shown
on member cards so component optionality cannot hide the name-or-identifier rule.
Related-field links do not imply automatic dependencies or derived values.

Review the outline, terminology, field cards, narrow-screen behavior, keyboard
navigation, and deep links before expanding the design to other sections.
Specification YAML, source transcriptions, identifiers, and records are unchanged.
Published assets and release metadata are unchanged. The guide is a review
prototype, not a new published release or a full accessible-site certification.
