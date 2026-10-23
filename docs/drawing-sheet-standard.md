# KA roof support layout drawing standard

Current standard: 23 October 2026. See `roof-support-layout-workflow.md` for the
interpretation process. Prior site examples are not new-project engineering data.

## Sheet and metadata

- ISO A3 landscape; bordered drawing area; notes, structural member key, revision
  table, consultant/client panels and project title block on the right.
- Roof title: **Roof Support Layout**, in the title block. No duplicate plot title,
  status banner, source footer or revision narrative unless requested.
- Use KA branding and the correct project-client logo, with asset provenance.
  Request/store source artwork early; do not silently redraw or misattribute it.
- Populate site/address, client, project/drawing numbers, author, checker, revision
  and date from project instructions. AT/AF and revision 01 are Honeypot issue
  values, not global defaults. Metadata does not itself establish sign-off.
- Place the KA compass at the top-right of the drawing frame, orientated from the
  supplied GA using the same plan transform. Keep it clear of border/title block.

## Geometry, dimensions and key

- Use black lines and text, distinguishing geometry by line weight and line type.
  Confirmed load-bearing building boundary and stair walls use a heavy solid line.
  Background/reference geometry is lighter. Sketch symbols follow the current key.
- Keep numeric dimensions in millimetres, without INT/EXT suffixes. Reference faces
  or centrelines are established by extension origins, retained in structured data.
- Thin black extension lines and arrowheads; consistent readable black text near
  the relevant area. Align dimension chains. Do not use prose as a substitute.
- External dimensions/gaps attach to actual outer wall faces. Internal dimensions
  attach to inner faces; beam-to-beam dimensions follow the established centreline
  convention unless contradicted by the survey. Never replace dimensions by scaling.
- The key includes only relevant members/walls/line types. Include supplied section
  specifications. Do not retain removed window/equipment/door explanations or the
  phrase "Engineer-described survey line". A suitable confirmed-wall key label is
  "Load-bearing walls — External boundary and stairs" where applicable.
- Keep notes short and site-relevant. Record evidence links, interpretation history
  and detailed uncertainty in the project file rather than cluttering the plan.
  Unconfirmed engineering information must still remain distinguishable.

## Deliverables and separation

One dedicated roof-layout sheet. Chimney elevations and telecom/connection details
are separate workflows awaiting instructions; do not automatically bundle them
into future roof-layout exports. Existing worked detail sheets remain separate.

PDF and requested DWG must agree in content, units, personnel and revision. PNG is
an optional preview. Check text fit and inspect both the PDF and a CAD rendering.
Audit CAD conversion for lost entities, text, colour and dependencies. Declare an
A3/NTS sheet-space DWG as such; it is not a full-size building model. Retain current
canonical output names and clear scoped superseded generated files when requested.

## Existing implementation

`sheet_template.py` formats an engineering plot using a project profile and
`assets/branding/registry.json`. Its hide-title/banner/footer options and compass
placement support this format. The site renderer determines engineering geometry;
the formatter does not interpret surveys. Older Asmer colours, beam counts and
metadata are historical example settings, not the current global presentation.
