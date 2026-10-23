# CAD-Maker project instructions

For roof support layout work, read these before interpreting inputs or drafting:

1. `docs/roof-support-layout-workflow.md` — current end-to-end roof layout process.
2. `docs/roof-support-layout-rules.json` — reusable rule identifiers and defaults.
3. `docs/drawing-sheet-standard.md` — KA presentation and export requirements.
4. The current project's `project.json`, source register and decisions — engineering facts and latest corrections.

Start each new site from `templates/roof-support-project.json`. Never import another
site's dimensions, building geometry, structural classifications, member sizes,
flat numbers, personnel, client or revision as defaults. The template and rules are
reusable; prior site records are examples, not evidence for the new site.

The current agreed workflow is **Roof Support Layout only**. Chimney elevations,
telecom frame/connection details, tripods and EMA details belong to separate
workflows awaiting the engineer's instructions. Retain their evidence without
letting detail generation become a dependency of roof-layout delivery. Do not
assume a page number always identifies a particular drawing type.

Use current engineer corrections; do not repeat answered questions. Inspect source
labels, keys and attachments before asking. Batch precise unresolved questions and
continue independent work. Respect an explicit hold on regeneration/publication.

Use written survey dimensions. Never derive replacement engineering dimensions by
scaling a PDF or photograph. Graphic GA transformations and vector extraction are
allowed to identify, place and export the correct reference geometry.

The site renderers and prototype are worked implementations; the saved workflow
is a specification and reusable working instruction, not a claim that arbitrary
site interpretation is already automated. Preserve original sources and decisions.
When asked to clear superseded documents, clear the scoped generated deliverables;
do not erase evidence, other projects or rewrite Git history without instruction.
