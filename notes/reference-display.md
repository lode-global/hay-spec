# Reference display configuration

`reference-display.yaml` supplies optional human-readable titles for nodes without
canonical titles and navigation groups for the nutrient reference page. It is a
presentation overlay, not part of the hay-record format. Consumers may reuse it
for labels without changing their records.

Title keys use slash-separated ancestor identifiers, including the section.
Dotted component identifiers and percent signs are literal: do not normalize,
split, or rename them. Existing canonical titles cannot be overridden. The
generator rejects unknown title keys, ambiguous paths, empty titles, and stale or
out-of-order navigation starts.

Each nutrient group starts at an existing direct field and continues until the
next group. Groups follow source order and add headings and linked contents only;
they do not create record containers. All identifiers remain visible and existing
explicit node anchors are retained. The canonical YAML and its JSON transcription
are unchanged. Group names are navigation aids, not new scientific classifications.

Edit this configuration and run `python tools/generate_docs.py`, followed by
`python tools/generate_docs.py --check` and `mkdocs build --strict`. Supply
`--display PATH` to use a different configuration. CI checks the tracked overlay.
The published v0.92.0 assets remain the immutable release snapshot; these labels
are current-reference improvements and do not change publication metadata.
