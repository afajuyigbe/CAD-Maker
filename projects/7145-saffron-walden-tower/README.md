# 7145 – Saffron Walden Tower

Revision 1, review package, 4 November 2026. Client JetNSL; drawn AT, checker field AF. The checker field identifies the nominated checker and does not record completed checking or approval.

## Drawing set

- 7145-01: Roof Support Layout with the single soffit-scan marker. The separate flange-9 section and wall-offset detail have been removed.
- 7145-02: Dimensioned sectional elevation, tower and fourth-floor interior 3D views. The B1 specification is retained in drawing note 2; its separate section is removed.

This corrected two-sheet set supersedes the initial three-sheet review. The standalone scan sheet is withdrawn.

The combined PDF and DWG contain both sheets. Individual PDFs/DWGs and editable DXFs are also included. Keep the two rendered PNG files beside the DWGs/DXFs for their relative image references. The 3D sheet also contains editable visible feature-edge linework.

## Coordinates and model

Sheet CAD files use millimetres in A3 sheet space and are NTS; do not measure building dimensions from these files. The separate 7145-tower-model DWG/DXF and STEP use full-size millimetres, Z up. The origin is the southwest internal corner at ground datum before applying the GA plan rotation of 3.165 degrees counterclockwise. Positive X/Y correspond approximately to east/north. Exact transformation and review parameters are in model/parameters.json.

The STEP is a named surface assembly, not a fabrication solid model. Mesh geometry and review renders share the same source. The engineer requested OBJ/MTL export and GitHub publication on 4 November 2026 after the marked corrections. The matching OBJ/MTL use the same millimetre/Z-up coordinate system and relative material-library path, with self-contained flat colours.

## Confirmed support and scan information

The clear internal plan is 5200 x 5200. Seven internal wall-to-wall embedded beams divide it into eight 650 mm spaces, with no edge beams. Roof slab thickness is 175 mm and parapet height 550 mm. Embedded beam sections were not measured and are represented by position bands at the soffit.

Primary beam B1 is 510 deep x 190 wide, flange 20 mm, at the FLOOR of the fourth floor / ROOF over the third floor. It does not support the roof above the fourth floor. The fourth-floor roof member profile is 152 deep x 125 wide, flange 9 mm. A reliable standard-section designation has not been established; the measured profiles are retained for review. Web thicknesses in the visual model are unmeasured proxies, not specified dimensions.

The ribbed fourth-floor panels belong to the decommissioned water tank. They and the large flanged service pipe are not classified as structural building columns or roof supports. Scan location 1 targets the roof soffit over this floor; the numbered references 1–3 on the survey sketch are member/detail references, not three scans.

## Review interpretation

The sectional elevation dimensions the six floor-to-ceiling clear heights separately: 5600, 2400, 2600, 5500, 2800 and 4100 mm. The 175 mm concrete slabs are drawn and dimensioned independently of those clear heights. The intermediate timber deck and fourth-floor steel-deck build-ups have not been measured and are schematic, without invented thickness dimensions. B1 is shown as a downstand at the fourth-floor floor.

No cumulative absolute floor levels are inferred from the incomplete build-up information. The GA main roof +25.00 m AGL is retained for the visual model; its fourth-floor floor is 4100 mm below the 175 mm roof slab soffit (+20.725 m in model coordinates), rather than forcing the GA RRU-plan level +20.70 m to be an exact surveyed floor level. The elevation is NTS and uses the independent clear-height datums recorded in elevation-datums.json. Facade proportions, unmeasured wall envelopes, arch details, hatch/stair, tank modules, pipe and connection details are visual interpretations of the supplied photographs. Exposed roof member positions are schematic from the sketch, without a surveyed set-out dimension. The primary E/W member position within the floor is also schematic.

The three 150 mm wall returns and lowest 300 mm return are applied to the actual lower-plinth envelope in the section and 3D model, beneath the lowest arched openings; the upper shaft remains constant in width. The 20-course intervals are retained. The top of the lower-plinth step sequence is aligned with the first-floor level (5600 clear height plus 175 slab). The 20-course spacing is graphical: its nominal course pitch is derived from that plinth height, not a surveyed brick dimension. No millimetre height dimensions are issued for the wall steps. Decorative cornices are separate from the widening wall body. The roof-plan repeated 650 mm chain and all spacing/no-edge-beams notes are removed as requested; the beam geometry and 5200 clear dimensions remain.

The explanatory interior perspective shows the 3700 mm tank panels, the 400 mm exposed-brick band above (4100 clear room height less 3700 tank), and the roof soffit. Floor beams, the access opening, pipe and stairs are omitted from this view to keep that relationship clear. Its simple unbroken floor surface is a view-only illustration group, excluded from full-size STEP/DWG/DXF exports and from the whole-tower render; OBJ export also excludes interior_review groups. The actual access and floor geometry remain in the full model.

The model includes nine allocated TEF panels in three sectors, fifteen allocated internal RRUs, a 300 mm allocated dish and retained OLO roof equipment. Equipment arrangement follows the GA graphically; unmeasured bracket details are for arrangement review. The allocated dish bearing is unspecified in the GA and remains a visual placeholder. No connection capacity or structural design is inferred.

## Validation

Checked two A3 PDF pages, metadata, text bounds, all six clear-height endpoints, separate concrete-slab dimensions, the B1 level in both section and model, three 150 mm plinth offsets and one 300 mm return with a constant-width upper shaft, the 8 x 650 closure, seven beam axes, no edge beams, one integrated soffit-scan marker, absence of a separate scan sheet, and equipment counts. All exported CAD entity counts, text, layout names and image references survived DWG-to-DXF readback. The readback parser normalized three unsupported default material dictionary placeholders; these do not encode the drawn geometry or render colours. Independent CAD sheet previews were inspected. STEP and mesh bounding boxes agree. Validation details are in validation.json.

## Sources

GA: CS_111051_TEF_8233_VF_75548_GA_REV_1A (1).pdf, revision 1A, 20 pages. Survey Notes.pdf, 4 pages. Engineer clarifications and supplied external, rooftop and fourth-floor interior photographs. Source GA project numbers and revision are distinct from project 7145 / drawing revision 1.

Dimension terminators use compact diagonal ticks in both PDF and CAD, replacing the overlapping open arrows at adjacent floor/slab datums.

## Final base and wall dimensions

The engineer clarified an 8000 mm external masonry width right at the bottom and 1400 mm base walls around the 5200 mm clear interior. The reduced wall thickness is described as approximately 550/600 mm by the FIRST floor, superseding the earlier top-floor reference. The elevation carries that approximate label. Exact closure of the 8000/5200 widths with three 150 mm offsets and a 300 mm return gives a nominal 650 mm shaft wall in the geometry. This nominal closure value is distinguished from the engineer's approximate field estimate; no additional projection or hidden return has been invented. The 8000 dimension terminates on the bottom masonry faces, not on decorative cornice projections above the bottom.
