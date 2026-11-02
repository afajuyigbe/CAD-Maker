5166 — TADWORTH HOUSE
Skye Consultants | ST / AF | Revision 1 | 2 November 2026

REVIEW DRAWINGS — THREE A3 SHEETS
01 Roof Support Layout
02 Roof / Top-Floor Supports: roof/top-floor view and cutaway with roof omitted
03 Scan Locations
The former standalone rooftop-only sheet is removed.

DWG FILES
5166-drawing-set.dwg: three named A3 layouts. Keep the two supplied PNG views beside this DWG for the page2 rendered underlays. Roof and scan sheets use editable vector geometry.
5166-roof-support-layout.dwg and 5166-scan-locations.dwg are standalone editable sheets in A3 sheet millimetres, NTS.
5166-building-model.dwg is full-size3D surface geometry in millimetres, separated by component layers. It is distinct from the drawing-set DWG. Use an isometric/3D view to inspect it.

EDITABLE MODEL
5166-building-model.step contains independently editable component surfaces, not a closed solid or a native feature/history tree. model-source/model/ contains the geometry builder, parameters and shared mesh used for the render views; Python/CadQuery dependencies are needed to regenerate it.
The editable model retains the lower building in lower detail. Page2 focuses on the roof and top floor and does not show the building down to ground. The second view intentionally omits the roof to reveal top-floor supporting members; it is a cutaway, not an actual opening.

TELECOMS ARRANGEMENT
Each sector has a single central braced mast and yoke brackets: one H3G antenna on one carrier, with the two EE antennas stacked on the other. Current proposed equipment is included; future transmission dishes remain omitted.

GEOMETRY BASIS
X east; Y north; Z up. Ground datum0; main roof26100; plant-room roof27420mm.
The roof layout uses the engineer's marked walls/beams/columns and confirmed dimensions. Unmeasured facade details, upper-floor level and member cross-section envelopes are visual review geometry, not an as-built or fabrication survey.
OBJ/MTL exported from the engineer-approved review geometry. Keep 5166-tadworth-house.obj and 5166-tadworth-house.mtl together. Import as MILLIMETRES with Z UP; OBJ does not encode unit settings. Materials use self-contained flat colours; no texture images are required. The OBJ contains the full building, including the lower-detail lower storeys; page2 views focus on the top floor.

SCAN LOCATIONS
1:topside+soffit;2/3/4/9:soffit;5/6:topside;7/8:general.
Opposing diagonal hatch directions denote topside/soffit, crossed hatching denotes both, and a plain square denotes general. The scan page omits room labels and dimensions.

NORTHEAST TERRACE UPDATE
The eighth-floor northeast terrace is enlarged into a continuous wraparound area, including the space outside the upper roof corner. The upper roof/support plan is unchanged. Scan1 is lower/both; scan2 is upper/soffit.

REGENERATION SOURCE
The model-source/model/ folder contains the approved mesh, geometry builder, renderer and OBJ exporter. The adjacent model-source/drawings/ folder receives regenerated CAD/OBJ outputs. Python, NumPy, Pillow, ezdxf and CadQuery are required.
