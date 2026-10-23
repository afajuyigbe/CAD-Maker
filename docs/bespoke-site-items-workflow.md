# Bespoke site items: 2D drawings and 3D views

Version 0.2 — output selection required before starting, 23 October 2026.
Authority: engineer's instruction and two supplied presentation examples.
This specifies the workflow; it does not claim that a general modelling engine
has been implemented or that a real item has already been modelled.

## Purpose and inputs

Produce dimensioned 2D plans and elevations and a corresponding 3D rendered view
of a surveyed item or primary structure. Examples include chimneys, tripods,
buildings, water towers and other bespoke site structures. This is a separate
workflow from Roof Support Layout, with shared KA branding and drawing standards.

The engineer supplies photographs and dimensioned sketches. A GA, existing detail
or other supplementary information may also be used when supplied. A GA is not a
mandatory prerequisite for modelling a standalone item.

The two example images define presentation intent: clear annotated plans and
vertical views, plus a clean technical 3D view. Their geometry, materials, dimensions,
scale and connections are not facts for any new item. The first example also
illustrates different-level plans and a section: provide those additional views
when necessary to describe the actual structure, rather than copying its view count.

## 0. Confirm outputs before starting each item

Ask the engineer what is required before starting item interpretation, modelling,
drafting or rendering. Do not assume the full package from a previous item. Offer
3D model only, 3D model plus rendered view, or a combined 2D/3D drawing package;
allow a specific selection of outputs. If the current instruction already states
the required outputs clearly, record that answer without asking it again.

Record whether PDF, DWG, plans/elevations/sections, editable 3D model and rendered
image are requested. Confirm the model/export format and sheet arrangement only
where applicable. An editable model and a rendered image are different outputs:
"3D model only" does not request drawings or a rendered image.

Do not begin the item work until the output selection is confirmed. Perform only
the stages needed for that selection. For model-only work, omit 2D views, drawing
sheets, PDF/DWG drawing exports and rendering unless separately requested.

## 1. Register and reconcile the evidence

Create an item identity within its project, using `templates/bespoke-site-item.json`.
Register original photos, sketches, page/region references, units, revisions and
any earlier drawings. Reuse the project's confirmed client and issue metadata;
do not inherit another site's facts.

Use photos to understand form, arrangement, visible construction, materials,
openings, supports and connections. Use the sketch's written measurements to
constrain the geometry. Do not obtain replacement dimensions by scaling perspective
photos, a PDF, a sample render or an estate-agent plan. Photogrammetry is not implied
by receiving photographs. Distinguish existing and proposed work where relevant.

Label faces and photo directions consistently. Establish an origin, axes, units
and level datum for the item; these need not be geographical north. Associate each
measurement with its actual faces, centrelines, edges, levels or member endpoints.
Register access limits and hidden construction.

## 2. Build a dimension and feature register

Transcribe overall lengths, widths and heights, levels, wall/slab thicknesses,
member sections, offsets, tapers, apertures and visible connections as applicable.
Record each value's evidence and status: measured/source-observed,
engineer-confirmed, derived, estimated, unresolved or superseded.

- Written dimensions govern. Keep internal/external/centreline references in data;
  printed dimension extensions identify those references without INT/EXT suffixes.
- Reconcile overall/component dimensions and repeated measurements before modelling.
  Derivations require established parent values and compatible datums.
- Do not assume a centred taper, symmetric supports, equal faces or uniform wall
  thickness without evidence. Rectangular chimney faces may need separate elevations.
- Do not manufacture bolt counts, anchorage embedment, hidden reinforcement, member
  grades, masonry strength or support conditions. Dimensions do not establish capacity.
- A visible material finish is not proof of structural material specification.
  Estimated slab thickness remains estimated, even in a realistic-looking render.
- Ask one small batch of precise questions about conflicts or missing values that
  affect the model. Inspect the sketches/photos first; retain answers and update
  all dependent geometry. Progress independent work while answers are pending.

An unresolved feature must remain absent, explicitly schematic or qualified as
instructed. Do not silently invent its geometry to make the model look complete.

## 3. Construct one coherent geometry model

Create one dimension-controlled representation in actual units, normally
millimetres at 1:1 model size. Keep solids/members/openings as identifiable parts,
with levels, face IDs and dimension dependencies. Separate survey facts from
presentation choices such as colours, camera angle and exploded/cutaway settings.

The model is the common source for all plans, elevations, sections and renders.
Do not independently sketch a convincing 3D image that disagrees with the 2D views.
An image-generation prompt is not a substitute for dimension-controlled engineering
geometry. Use appropriate CAD/modelling and rendering tools for these outputs.

## 4. Generate the dimensioned 2D views

When 2D drawings are requested, the usual starting views are plan and elevation,
subject to the confirmed brief. Skip this stage for model-only work. Choose the elevation that best explains the
item; add the opposite/orthogonal face, additional level plan, or section when the
geometry cannot be communicated clearly in the minimum pair.

- Project the same model into orthographic views with consistent axes and levels.
- Use section markers, view titles, face IDs and levels when relevant. Different
  floor/roof plans remain distinct; sections expose actual specified features.
- Include sufficient overall and local dimensions to define the supplied geometry.
  Extension lines must reach the correct actual faces/centrelines.
- Use black dimensions, text and CAD linework, a clear line-weight hierarchy and
  suitable material/section hatching. Keep dimensions clear of geometry and one another.
- Include supplied member specifications and concise necessary notes. Clearly label
  estimates or unresolved information that would otherwise look definitive.
- Choose a legible scale for the view and sheet. Dimension values remain true model
  measurements. Never label a schematic/unknown geometry view as accurately scaled.

## 5. Produce the matching technical 3D view — when requested

Skip rendering when only an editable model is requested.

Render an isometric/axonometric or suitable perspective view from the same model.
Use the supplied example's technical character: clean white background, defined
edges, restrained material colours/textures and a camera that explains the structure.
Avoid decorative effects that obscure structural members or imply unverified detail.

Show modelled openings, levels, supports and components consistently with the 2D
views. Where appropriate, use a separate labelled section/cutaway to reveal internal
arrangement; do not depict it as an actual physical opening. Do not hide a critical
member solely to improve the appearance. Do not infer material strength or structural
capacity from the render. Dimensions are read from the 2D views, not from perspective.

## 6. Compose the KA sheet(s) — when drawings are requested

Skip sheet composition for model-only work.

Reuse the KA border, client/consultant branding, notes/revision area and title block.
Use an item-specific title and drawing identifier; do not title a chimney or water
tower sheet "Roof Support Layout". Author, checker, revision and date come from the
current project instructions. Add a compass only where relevant to the view.

Place plan, elevation and 3D view on one sheet **when legible at the selected scales**.
If the structure, annotations or number of required views is too large, use
additional sheets with consistent identifiers/revision and clear cross-references.
Do not reduce dimension text or critical detail to force everything onto one page.
A 3D view is not required to be on a separate sheet.

## 7. Check and export

Verify the following before issuing:

Apply the following checks to the selected outputs; cross-view and sheet checks
are not applicable when those outputs were not requested.

1. All supplied dimensions/features are represented, explicitly unresolved or
   excluded with a reason, and refer to the right datum.
2. Shared measurements, overall/component sums, levels, thicknesses and offsets
   reconcile; estimates retain their status.
3. Plan, elevations, sections and the rendered view describe the same model.
   Check asymmetric/tapered parts and face orientation explicitly.
4. Required features and notes remain visible; view labels, section markers, scales,
   units, title block and revision agree across formats.
5. Check the actual PDF, CAD export and 3D render for clipping, missing geometry,
   readability and external asset dependencies. Audit a conversion round-trip where used.

Deliver **only the outputs confirmed for this item**. Available outputs are PDF
drawings, DWG drawings, an editable 3D model and a 3D rendered view. A full package
contains all four; a model-only commission contains only the editable model.
When drawings and rendering are requested, embed the rendered view on the
sheet where appropriate; provide its image separately when useful. The model
must retain editable geometry, not just a flattened image or a viewer-only file.
Retain native/source geometry where available. Select a suitable editable/exchange
format for the actual item and the engineer's software when the first item is
prepared; the specific format has not yet been chosen. Do not imply that a neutral
solid exchange retains a native feature/history tree if it does not.

A true-size item model is distinct from the earlier roof workflow's A3/NTS sheet-space
DWG export. Label CAD model/paper spaces and units accurately; do not imply that a
sheet-space file is a full-size model. Match the actual capabilities of the chosen tool.

Replace current issue files and clear scoped superseded generated deliverables when
requested. Preserve original evidence, decisions and other items/projects. Keep a
single dimension/model record and batch downstream exports to minimise rework.

## Initial worked-item milestone

First confirm the outputs for one actual item. If the full package is selected,
use its photos and dimensioned sketch to complete the chain: evidence register -> resolved geometry -> plan/elevation -> matching 3D view
-> composed sheet and requested exports. Establish acceptance on that final product
before building a broad application or testing many unrelated items. The presentation
examples alone are not sufficient evidence to generate a new site's geometry.
