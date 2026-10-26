# One Field Guide reading experience

The Field Guide is the public entrance and primary field reference. Every source
node carries its exact parsed source object and now exposes it in a collapsed
“Complete source definition” disclosure. No properties are filtered from that
view. Nested members remain individually navigable; the disclosure also retains
all children for exhaustive inspection. YAML comments remain in the canonical
download, not the JSON transcription or parsed-source disclosure.

The About page retains the former overview's complete front matter, naming and
validation conventions, source digest, publication context, and known source
warnings. Only its section links change to field guides. Supporting guidance and
history use the same header, palette, typography, card surfaces, and primary
navigation; a Guidance and history index replaces the crowded navigation tabs.
MkDocs remains the build machinery for these pages and downloads. The interactive
guides retain their section search. The separate Material site-wide search and
sidebar are no longer exposed; the field outline and guidance index provide the
reader navigation instead.

Existing technical pages remain generated unchanged as no-JavaScript fallbacks,
not a second normal reading destination. With JavaScript enabled, `/fields/…/`
links forward to the matching guide. Explicit source anchors and automatic
heading anchors map to the appropriate field, including literal dots and percent
signs. Unknown anchors retain the original reference page rather than silently
pointing to another definition. `/technical/` and old overview heading bookmarks
forward to the equivalent About headings. `/guides/` and `/guides/index.html`
forward to the single home entrance, retaining their index as a no-JavaScript
fallback. Relative destinations support hosting under a repository subpath.
Redirects use replacement history entries to avoid a Back-button loop.

No canonical definition, identifier, enum, type, constraint, record structure,
source metadata, archived note, or published asset is changed. Technical Markdown
files and YAML/JSON specification downloads remain byte-identical. Coverage tests
compare every source node, every stable legacy anchor, and the full overview
content. Browser checks cover redirects, disclosures, guidance, and the shared
reading shell. This change does not deploy the site, tag, or publish a release.
