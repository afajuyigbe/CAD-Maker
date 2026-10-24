# Whole-building visual model workflow

Working instructions agreed through Honeypot Hall and River House, 24 October 2026.

1. Confirm project, model scope and outputs. Use a separate project folder. Whole-building modelling is distinct from dimensioned roof-support drafting and bespoke-item engineering details, although requested views can be combined into a drawing set.
2. Register GA, written dimensions/levels and photographs. Distinguish street/rear/end facades, roof levels, parapet tops and neighbouring roofs. Use photographs for visible arrangement and explicitly qualify estimated grids, equipment sizes and hidden details.
3. Construct one surface geometry source for review renders and eventual exports. Use measured roof values where supplied. Do not fabricate concealed connections or assume structural capacity. Keep unverified embedded member sections unverified. Distinguish primary structural column lines from secondary curtain-wall mullions, and carry confirmed column continuity through the model. Preserve photographed antenna groupings and shared bracket arrangements; do not replace paired panels with a single panel by default.
4. Verify handedness against asymmetric GA landmarks. Apply the same orientation to geometry and compass; an image-axis inversion in a plot must not mask a mirrored model. Avoid diagonal roof tessellation edges where rectangular surface panels suffice.
5. Produce review images/sheets from that geometry. Check facade correspondence, roof equipment, cropping and material visibility. Inspect CAD conversions visually as well as checking text/geometry retention. Keep drawing sheet units distinct from actual 3D model units.
6. Obtain engineer approval of the 3D geometry and rooftop arrangement BEFORE finalising/issuing OBJ and MTL. This review gate was explicitly requested by the engineer on 24 October 2026. Working geometry may be prepared for review, but it is not an approved export. Incorporate corrections and preserve the approval record.
7. After approval, export OBJ polygon surfaces with the matching MTL from the same approved source. Document units/up axis/origin; prefer self-contained flat colours unless textures are requested. Validate indices, polygon areas, material references and an independent readback. Deliver the two files together and remove scoped superseded issued versions when requested.

Software may triangulate polygon faces internally. Explain feature-edge display where relevant rather than promising that arbitrary importers can suppress every tessellation edge.
