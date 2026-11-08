Delivery: use the **[delivery](delivery/)** folder. It contains only the complete drawing PDF, self-contained combined DWG, OBJ and matching MTL. Other folders contain working records.

# 71222 – Jet 0231

Revision 1, 8 November 2026. Client Jansen SL; drawn S.T.; nominated checker K.S.

## Drawing set

- 71222-01: Roof Support Layout, with distinct member patterns and the closed beam grid.
- 71222-02: Roof Equipment Layout, dimensioning PV arrays, hatch/skylights, safety line and parapet.
- 71222-03: Theatre context, roof-support cutaway and existing-roof 3D views.

The combined PDF/DWG contains all three sheets. Individual sheets and DXFs are included. Sheet CAD uses millimetres in A3 sheet space, NTS. Keep the three rendered PNGs beside the DWGs for relative image references. Editable visible feature edges accompany the 3D images.

The separate visual-model STEP/DWG/DXF is full-size millimetres, Z up. STEP is a named surface assembly, not fabrication solids. Roof structure and equipment share one parameter source. The surrounding theatre is simplified photographic context. No telecoms equipment or scan-location sheet is included, as instructed.

## Member graphics

Castellated members use paired long dashes. B1 I-beams use double continuous lines; B2 uses double short dashes. Member tags are omitted from the plan; the matching key identifies each symbol. CHS braces use single dash-dot chains. The full-web end beam uses a heavy continuous line. Safety uses a short dash/double-dot chain. These patterns, weights and matching legend samples are carried into both PDF and DWG; identification does not depend on member labels or colour.

The engineer confirmed five castellated axes with four3000mm centre-to-centre bays. The horizontal chain is2200+2500+4x3000+2500+1300+300+500=21300. The lastB2 is at20500, full-web member at20800, and right reference wall at21300. The main-depth brace chain is1700+4x1750+1900=10600, with the1900 corridor completing12500.

On6November2026 the engineer confirmed the castellated profile: **800mm overall depth,210mm flange width and18mm flange thickness**. The full-web end member uses that envelope without web openings. Castellated opening pitch/shape and web thickness remain visual proxies; no unmeasured web value is presented as an engineer specification.

The 8 November correction supersedes the previous all-upper CHS arrangement. In the left diagonal bay (x0–4700), CHS90 remains above B1/B2 at the castellated upper flange. Across the four central castellated bays (x4700–16700), CHS90 is lowered to the B1 beam level, near the lower castellated flange. Beyond the last castellated beam (x16700–20800), only the I-beams remain: no overlapping CHS. Central CHS uses the existing schematic B1 centreline (roof reference minus 750 mm minus half the 250 mm depth); this correction supplies the relationship, not a newly measured vertical datum. No connection plates, welds or bolts are invented.

**All orange I-beams are B1(200x250), except the three marked B2(200x150)** atx2200,19200 and20500. Three west-bay and five east-bay lower B1cross-members are now included. The west B1/B2 members are shown beneath the diagonal top CHS as in the annotated photograph. Existing750/350mm roof-offset readings locate the lower members schematically; exact top/centreline reference, I-section width/depth convention and unsupplied thicknesses are not newly claimed as verified. The model does not imply certified connection continuity between crossing members.

## Equipment set-out

Outside-edge roof references are used for equipment setbacks. PV west/east setbacks are3500/2900. From the farther corridor wall southward, the closed PV chain is:

2100 +1850 +1950 +1700 +1350 +1900 +1650 =12500.

The first hatch is12800 from the west edge, with its dimensioned south upstand face1500 from the farther corridor wall. The first skylight's west edge is3200 from the east edge. The closed opening chain is:

12800 +1300 +4000 +3200 =21300.

The engineer explicitly instructed the chains to be forced closed. Accordingly, the original1400 PV gap was normalised to1350 and the3900 hatch-to-skylight gap to4000. Those changes preserve the overall dimensions, array depths, corrected1950 gap, and edge setbacks. Original readings remain in the project decision history, with no closure-review flags on the sheets.

Hatch/skylight upstands are1300x1300 overall and300 high. The photo shows two separate glazed skylights adjacent to the parapet, distinct from the access hatch. White frames and inset glass are shown. Frame width and clear-aperture geometry are visual proxies, not additional measured dimensions; the second skylight's individual gap remains graphically placed because no separate measurement was provided.

The safety path is1500 from the outside building edge at north/east/south as sketched. It is represented in 3D as a roof-level line; an unmeasured physical barrier height has not been invented. The parapet is300 wide and300 high, with a dimensioned section on the equipment sheet. PV module subdivisions, tilt and mounting details remain illustrative; three rows are confirmed.

## Source and coordinates

No GA/native plan file was supplied. Geometry was reconstructed from annotated plan images and engineer corrections, with photographs supplying arrangement and visual context. Original image binaries are not available in the workspace; sources/register.json identifies the inline references without invented hashes. Engineering dimensions have not been obtained by scaling photographs.

Local positive X follows the21.3m direction and positive Y points toward the corridor/auditorium. The model applies a nominal39-degree graphical rotation from the annotated aerial north arrow; world positiveY corresponds to indicated north, and Z is up. This is a graphical reference, not a georeferenced survey bearing.

Building heights, wall build-ups and surrounding-theatre proportions are unmeasured visual interpretations. The18m roof-level datum is for the visual model; the provisional3.4HR note is used only as gallery-to-roof context. Fly bars, pulleys and suspension cables are excluded from roof-support members. The client panel uses Jansen SL as plain text because no client artwork was supplied; the KA logo is the supplied consultant asset.

## Validation

The package records A3/metadata/text-bound checks, closed beam/equipment chains, model member and equipment coordinates, CAD pattern and entity/text retention, image-reference resolution and STEP/mesh bounds. Independent CAD previews were inspected. Readback normalises unsupported default material placeholders; drawn geometry and image colours are retained. See interpretation/validation.json and the package manifest.
