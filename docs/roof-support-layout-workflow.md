# Roof Support Layout workflow

Status: agreed working procedure, 23 October 2026. Applies to any new site.
Owner: KA Engineering. Supporting rule IDs: `roof-support-layout-rules.json`.

## Scope

Create a professional roof support layout by interpreting survey notes, GA
information, photographs and supplementary references together. A cleaner copy
of the handwritten sketch is an intermediate interpretation, not the final product.
The final product places the interpreted support information and written dimensions
on the correct GA building outline in the KA sheet format.

This workflow covers the roof layout only. Chimney elevations and telecom steelwork
or connection details are separate processes that the engineer will describe.
Existing detail examples do not define those future processes. They must not delay
or automatically add sheets to the roof-layout deliverable. Retain roof-level
positions of such features when supported and relevant. Recognise document content
rather than assuming "page 2" or any other page number has a universal meaning.

## 1. Intake once

- Create `projects/<reference>-<site>/` with sources, interpretation, decisions and
  drawings folders. Use `templates/roof-support-project.json` for an empty record.
- Register original filenames, revisions, page counts and hashes. Record photos,
  including 360 images, and supplementary snippets separately. Cache useful page
  previews; index long GA sets once and select the relevant existing plan.
- Record project reference, site/address, client/logo, drawing number, author,
  checker, revision and date from supplied information. Ask for missing issue
  metadata together; never silently reuse another project's title block.
- Retain KA branding and the agreed sheet format. Save accessible client logo
  files early, with provenance and client association. Never substitute a different
  client's logo or claim prepared/recreated artwork is the original supplied asset.
- Read file titles and visible labels before asking which source belongs to which
  flat or area. Keep material that was supplied but cannot be inspected flagged.

## 2. Identify the building before fitting the overlay

- Inspect the actual GA existing building outline and north symbol. Distinguish
  external walls, inner wall faces, roof edges, equipment, handrails and adjacent
  structures. Preserve stepped returns where within the agreed roof scope.
- Select a connected perimeter from GA linework; check closure and every return.
  Engineer-marked wall lines resolve ambiguous outlines. Do not align a complete
  overlay to a nearby equipment/roof line and then propagate that error.
- Align the survey view and GA graphically. A rotation or page-coordinate transform
  locates references; it supplies no new engineering measurement.
- Record the chosen wall/face references so all dependent dimensions use the same
  entities. Use actual GA faces rather than provisional boxes or pixel offsets.

## 3. Interpret structure and access

- Read the survey key first. Identify walls, beams, columns, support relationships,
  openings, stairs and corridors from the source and engineer's clarifications.
- Do not give a dashed line a universal meaning: it represented longitudinal beams
  in one worked site and non-load-bearing corridor boundaries in another.
- Show confirmed load-bearing external and stair walls with the agreed heavy line.
  Other sites' wall classifications do not prove a new site's structural roles.
- Extract available member sizes and specifications, including units and thickness.
  Ask about illegible, missing or conflicting section sizes. Never replace an
  unknown section with a common/standard size or treat "likely" as confirmed.
- Record sketch continuity separately from structural moment continuity. Do not
  invent concealed beams, anchorage, member sizes or unseen connections.
- Check the access graph: corridor arms join correctly, stairs have the specified
  door destinations, and each flat entrance opens into the intended space. Check
  adjacent room walls that should meet. Door widths/handedness stay schematic if
  not supplied; private hallways and communal corridors must remain distinguishable.

## 4. Use supplementary evidence correctly

- Apply engineer-confirmed rotations, flat labels and composites. Latest explicit
  corrections supersede earlier placements, while their decision history remains.
- Estate-agent floor plans can inform approximate room topology and opening
  positions. They are not necessarily to scale and are not a surveyed interior.
  Do not require a metric fit, infer wall loads from line weight, or silently
  present graphically fitted partitions as measured geometry.
- Compare photos with plan openings: window groups, small bathroom windows, stair
  glazing, corners and entrances. Check that each window is on its external facade,
  not an internal flat interface. Photos do not establish aperture dimensions or
  hidden load-bearing structure. Retain access limitations.
- Separate levels. A plant-room footprint above a stair/flat layout is not a room
  on that lower level. Follow instructions on displaying or omitting its outline;
  omitted outlines still need accurate face references for any dimensions shown.

## 5. Build one dimension register and attach each value to entities

For every relevant survey dimension record its raw reading, normalised millimetre
value, source region, datum, two reference entities/faces and confidence. Preserve
internal/external/centreline metadata even though those suffixes are not printed.

- Wall dimensions terminate on the specified internal or external faces. The
  under-dot notation used by this engineer identifies an external dimension;
  confirm a changed or conflicting survey key before applying the convention.
- Beam-to-beam dimensions use the engineer's established centre-to-centre convention
  unless the current survey indicates otherwise. Wall offsets require the actual
  stated face; do not infer the datum from apparent spacing.
- External plant-room dimensions terminate on both outer wall faces. Plant-room to
  external-building-wall gaps terminate on their respective outer faces. A value
  labelled external in data is insufficient if its extension line hits an inner
  face or a provisional footprint box.
- Keep internal plant-room lengths, external depths, wall thickness and the offset
  to the building edge distinct. A wall thickness applies only to the stated wall.
- Derive a missing arithmetic component only when its parent values and shared
  datum are established; record the calculation as derived, not independently
  measured. Do not infer an external overall from incompatible internal values.
- Reconcile every source label: positioned, clarified/superseded, excluded with a
  reason, or explicitly unresolved. Prevent omissions and repeated ghost readings.
- Print numeric dimensions in millimetres without INT/EXT markers. Use black text,
  thin extension lines and clear arrowheads. Place them near the relevant area,
  align chains and keep labels clear of walls, door swings and room text. Use
  dimension lines rather than prose such as "horizontal corridor 4.600 long...".
- When a wall/face moves, recompute every dependent extension origin and endpoint.
  Store stable reference IDs, not independent copied endpoint coordinates.

## 6. Clarify only what remains unresolved

Inspect first, then ask a small, consolidated batch with page/region, the uncertain
reading or endpoints, and the practical consequence. Use a marked crop or named
wall/room references rather than vague axis questions. Do not ask for dimensions
already supplied, repeat a confirmed answer, or ask an obvious elimination question.
Accept "not visible", "not measured" and qualified answers as such.

Save the exact answer and normalised interpretation once. Update its dependants and
supersede the mistaken reading everywhere. Progress independent work while answers
are pending. An explicit hold pauses the named generation/publication step; accept
further corrections into the record and resume when authorised.

## 7. Apply the KA drawing standard and export

Use `drawing-sheet-standard.md`. Default drawing title: **Roof Support Layout**.
One roof layout sheet, A3 landscape, GA backdrop, right-hand notes/key/title block,
KA and project-client logos. No duplicate plot heading, status banner, source
footer or revision commentary in the drawing area unless specifically requested.
Use concise notes and a member key matching the actual symbols/line weights.
Keep detailed provenance, assumptions and question history in the project record.

Use the KA compass style, placed top-right within the drawing frame. Read north
from the GA and apply the same transformation as the plan; do not assume north is
up on the output or confuse a roof-level/elevation marker with the north symbol.

Deliver the requested PDF and DWG, with optional PNG preview/download ZIP. Maintain
consistent project/drawing number, revision, author and checker across formats.
State NTS where appropriate; never copy a sample's scale into an unscaled drawing.
A DWG exported in A3 sheet-space millimetres is not a full-size building model;
identify that distinction in delivery metadata. No native CAD dimension/3D model
capability is implied by editable lines and text.

## 8. Final checks and issue

- GA boundary is correct, complete and aligned with the interpretation.
- Structural roles and member specifications match evidence/engineer decisions.
- Room joins, corridor routes, stair/flat door destinations and external windows
  match the latest interpretation; different levels remain distinct.
- Every dimension is accounted for, on the right datum and physical face/centreline;
  chains reconcile and short/long extension endpoints reach their actual references.
- All drawing text/dimensions are black; the key matches the plan. No removed text,
  stale question, duplicate heading, clipped logo or label collision remains.
- Compass orientation, sheet metadata and units agree across files.
- Visually inspect PDF/preview. Check DWG round-trip entity/text retention, units,
  line weights and external dependencies; inspect a CAD render, not just file size.
- Replace current issue filenames when instructed; remove scoped superseded output
  PDFs, previews, CAD files, packages and manifests. Do not delete original sources,
  decisions, other projects or rewrite Git history as a side effect.

## Faster execution on subsequent sites

Use one intake, one cached source review, one geometry/topology pass, one consolidated
clarification list, one dimension pass, and one formatted review draft. Reuse the
sheet formatter, branding registry, compass, dimension style and checks. Reuse the
process, never the last site's geometry. Finish the actual drawing for review;
do not move on to testing another site in place of producing the current product.

Once topology and references are stable, regenerate/export as a batch rather than
publishing every minor annotation change. Apply a correction to the structured
record once, update all dependants, then check the final pair of formats. Track
actual elapsed time, clarification rounds, missed dimensions and rework reasons to
measure improvement; no unmeasured speed claim or model-training claim is implied.

`render_honeypot.py` and the existing prototype are worked implementations. This
saved workflow is reusable guidance; it does not mean a general site interpreter
has already been implemented.
