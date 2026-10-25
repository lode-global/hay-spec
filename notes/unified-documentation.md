# Unified documentation entrance and design (review PR)

The site root now opens the field-guide landing page. The complete technical
overview moves from `/` to `/technical/`; its contents are unchanged except for
relative links needed at the new address. All `/fields/<section>/` routes and
explicit field anchors remain unchanged. Existing `/guides/` pages remain
available. A small homepage script forwards legacy technical-overview heading
bookmarks to their corresponding headings at `/technical/`.

The technical reference and historical audit use the guides' green/cream palette,
system typography, card surfaces, focus outlines, and consistent navigation
labels. MkDocs retains its search, contents navigation, and responsive controls.
The landing page prioritizes guide cards instead of implementation metadata.

Download links are visible on the landing page, guides, and technical pages.
They target the unchanged canonical YAML copy and JSON transcription. JSON is not
JSON Schema or a hay-record validator. Current working-source downloads are
separate from immutable published releases; no tag or release is created here.

Source version, draft status, and unreleased-work context remain visible. No
source definition, identifier, enum literal, type, nesting structure, archived
history, publication metadata, or record format is changed. Presentation-only
snapshot tests account explicitly for the overview relocation; they continue to
compare every field-reference page exactly and all source downloads byte-for-byte.

Preview with the existing generator/check commands, strict MkDocs build, and a
local server for `site/`. Review the site root, a field guide, a technical section,
the historical audit, YAML/JSON downloads, and old overview bookmarks. The change
does not activate GitHub Pages or deploy anything publicly.
