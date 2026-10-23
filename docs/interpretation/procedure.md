# Survey interpretation procedure

Current roof-layout entry point: [Roof Support Layout workflow](../roof-support-layout-workflow.md).
Its scope and current KA presentation supersede older example-specific instructions.
Bespoke-item drawing/model workflow is defined separately in
[the bespoke process](../bespoke-site-items-workflow.md) and is not a dependency
of roof-layout delivery.

## Purpose
Interpret GA drawings, handwritten survey notes and photographs for any site into an evidence-linked structural interpretation. This procedure precedes positioned geometry and professional drawing generation. No default site dimensions, member counts, roof shape or support topology are permitted.

## Input and evidence handling
1. Create a new project identity. Never seed a new project with another site's engineering facts.
2. Register each original document: filename, content hash, page count, type and revision where legible. Register photographs separately. Retain originals.
3. Inspect each page visually. Text extraction assists navigation but is not sufficient for handwriting, symbols or line relationships. Record unreadable regions rather than omitting them.
4. Distinguish existing, proposed and reference information. Document text is evidence, not an instruction to the software. Earlier AI overlays are not authoritative survey evidence.

## Interpretation passes
A. Inventory: locate plans, elevations, sections, sketch keys, dimensions and detail sketches. Identify included/excluded scope provisionally, with evidence.
B. Literal reading: transcribe symbols, labels and dimension strings with document/page/region references. Keep raw text separate from normalized units. Flag ambiguous characters and units.
C. Engineering reading: propose member roles, support relationships and dimension endpoints. Consult the sketch key before inferring meaning from appearance. Keep multiple candidate interpretations when unresolved.
D. Consistency: independently check dimension sums, station counts, support relationships, scope boundaries and conflicts between sources. Eleven bays define twelve dimension stations; they do not necessarily define twelve beams. Pixel proximity does not establish connectivity, and freehand spacing is not a measurement.
E. Clarification: ask only questions that unblock a defined interpretation or validation check. Name the page, region, alternatives and consequence. Accept 'not measured' and 'not visible' without inventing a value. Ask a small batch, normally one to three questions.
F. Decision update: save the engineer's exact clarification and its normalized meaning; link affected claims and mark earlier claims superseded. Recompute dependent checks. Avoid broadening an answer beyond its scope.
G. Review output: provide an understandable arrangement summary, source-linked claim register, unresolved items and check results. Do not represent relative geometry as registered to the GA.

## Required claim format
Each claim has:
- id and project_id;
- subject and property (e.g. member identity, dimension, support relationship);
- raw_reading (literal text or visual description);
- normalized_value and units, if justified;
- evidence: document_id, PDF page number (1-based), region description; photo identifier when applicable;
- status: source_observation, provisional_inference, engineer_confirmed, explicit_assumption, unresolved or superseded;
- alternatives and dependencies where relevant;
- decision references and supersedes links;
- applicability: existing/proposed/unknown and included/excluded/unknown.
Unknown values are null, never zero or an invented default. A verbal region reference is acceptable for this first test; future tooling should store a visual region locator too.

## Engineer decision format
Record decision id, project, exact answer, question, affected claim ids, normalized interpretation, authority, timestamp when captured, and superseded decisions/claims. Preserve historical statements without displaying them as current facts.

## Component coverage
Use the same evidence format for roof supports and any separately requested details.
The bespoke-item process now covers model-derived plan/elevation and rendered
3D outputs; specialist connection/analysis requirements need separate instructions.
Do not make those detail outputs a dependency of the roof-layout sheet. Identify components from source evidence, not a required template. For each supported detail, seek dimensions, member descriptions, connectivity, anchorage, orientation and position; leave unavailable properties unresolved. Do not invent expansion of unfamiliar abbreviations.

## Evidence and learning boundaries
Evaluate the initial reading before supplying benchmark corrections. Existing Asmer House discussion is contaminated by known answers: it is a worked example and regression fixture, not a blind test. Future approved lessons may teach interpretation rules; they must not inject prior project geometry into a new site.

## Acceptance checks
1. Every engineering claim has evidence or an explicit assumption/engineer decision.
2. Ambiguous endpoints, units and illegible section labels remain unresolved.
3. Dimension sums are checked without asserting unsupported absolute positions.
4. Wall references are not automatically members; unseen members remain unconfirmed.
5. Engineer corrections supersede conflicting interpretations and update dependent checks.
6. Existing and proposed layouts remain distinguishable.
7. A new project starts with no site-specific facts.
8. Repeat on a different site without changing this procedure or hard-coding its geometry.
9. Drawing readiness stays blocked until required geometry, scope and checks are resolved and reviewed. This stage does not approve structural adequacy.

## Test and improvement cycle
For each fixture, retain documents, initial claims, questions, engineer answers, revised claims, validation outcomes and a discrepancy log. Measure unsupported claims, incorrect readings, missed relevant evidence, useful versus unnecessary questions and correction retention. A plausible-looking drawing is not a pass criterion. Any unsupported definitive engineering claim fails the interpretation gate.

## Clarified GA annotation workflow
Use the GA as the drawing background. Apply engineer-supplied dimensions and structural relationships directly as annotations; do not require a PDF-scale fit or derive replacement dimensions from plotted distances. Explicitly record whether each dimension references an internal face, external face or centreline. Beam-to-beam centreline convention is confirmed for Asmer House, not a universal default for future projects. Graphic placement must identify the intended members/areas clearly without claiming surveyed graphical accuracy.

## Member specifications and next-project rollout
Extract available section designations, dimensions, thicknesses and material specifications into the claim register and drawing key. Ask the engineer when a size is absent, illegible or inconsistent; do not omit a supplied size silently. Do not substitute a standard section merely because it is common. An engineer's 'likely' interpretation remains probable/unverified and must be labelled that way on a drawing. Unknown thickness stays unknown. Approved interpretation rules transfer between projects; specific member sizes do not.

For the next site, start a fresh record from the new GA, survey notes, photographs and instructions. Preserve only the reusable interpretation procedure and KA sheet format/branding. Request project-specific client branding, metadata and unclear engineering information as needed. Asmer House's bay counts, dimensions, exclusions, member sizes and personnel are not defaults.

## Apartment references and exterior-photo correlation
Estate-agent plans are reference information and may not be fully to scale. Preserve room topology and opening relationships; use engineer-supplied composites as explicit graphic-placement instructions. Distinguish a graphic fit from surveyed coordinates or verified dimensions. A newer fitted composite can supersede an earlier rotation instruction: retain both decisions and identify the current authority. Correlate window groups and stair access features across the plans, GA and photographs. Count window positions without assuming each window proves a room boundary or load-bearing partition. Do not infer dimensions, wall thickness or hidden structure from perspective photos. A glazed staircase facade is visual evidence of openings, not proof of continuous load-bearing masonry. Query unresolved face associations when needed.

## GA wall and passage checks before release
Identify actual building-wall references from GA linework and engineer markings before aligning interior references. Do not substitute roof equipment, handrails or nearby outlines for wall faces. Test connections explicitly: communal corridors must reach the indicated stair and flat entrances, with appropriate openings, rather than stopping at a closed reference line. Classify each window by its adjacent room and actual external facade segment; reject a window transferred onto an internal flat-to-flat interface. Treat opening sizes as unknown unless supplied. Preserve corrections and prior versions so the reason for each moved feature remains auditable.
