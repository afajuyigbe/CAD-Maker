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

For bespoke items (chimneys, tripods, buildings, water towers and similar), read
`docs/bespoke-site-items-workflow.md` and `docs/bespoke-site-items-rules.json`.
Use `templates/bespoke-site-item.json` for a new item. Before starting each item, ask which outputs are needed unless already explicit.
Record the answer before interpretation/modelling/drafting/rendering; a 3D-model-only
request does not require 2D views, sheets or renders. Where requested, the same model
supplies the plan/elevations/sections and matching technical 3D view; combine views
on a sheet when legible. The scope is distinct from Roof Support Layout. Specialist connection
or analysis requirements still need their own evidence/instructions.

Shared KA presentation conventions transfer, but the roof-specific title, NTS
sheet-space geometry and mandatory site compass do not automatically apply to an
item drawing. Do not assume a page number identifies a particular drawing type.
Deliver only the confirmed PDF/DWG/model/render outputs. Select a suitable model
format when an editable model is requested; never assume the previous item package.

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

For whole-building visual models, read `docs/whole-building-visual-model-workflow.md`.
Submit the 3D geometry/rooftop review for engineer approval before finalising or
issuing OBJ/MTL. This is the engineer's explicit review gate, not a default approval
requirement for other work. Preserve measured facts and qualify photographic estimates.
