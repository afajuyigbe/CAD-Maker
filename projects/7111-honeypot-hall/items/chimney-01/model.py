"""Editable parametric exterior-envelope model. All lengths are millimetres.
The capped envelope is not a survey of internal masonry/flues or a capacity model.
Cap dimensions are authorised estimates; see model-parameters.json.
"""
import json
from pathlib import Path
import cadquery as cq
HERE=Path(__file__).resolve().parent

def build(parameters=None):
    p=parameters or json.loads((HERE/'model-parameters.json').read_text())
    h=p['brickwork_height_mm'];assert h is not None and h>0
    body=(cq.Workplane('XY').rect(p['base_x_mm'],p['base_y_mm'])
          .workplane(offset=h).rect(p['top_brick_x_mm'],p['top_brick_y_mm'])
          .loft(ruled=True,combine=True).val())
    c=p['cap'];width=p['top_brick_x_mm']+2*c['projection_x_mm'];depth=p['top_brick_y_mm']+2*c['projection_y_mm']
    cap=cq.Solid.makeBox(width,depth,c['thickness_mm'],cq.Vector(-width/2,-depth/2,h))
    assert body.isValid() and cap.isValid()
    return p,body,cap

def export(out=None):
    out=Path(out or HERE/'drawings');out.mkdir(parents=True,exist_ok=True)
    p,body,cap=build();assembly=cq.Assembly(name='7111_Chimney_External_Survey_Envelope')
    assembly.add(body,name='Brickwork_Exterior_Envelope_Internal_Voids_Not_Surveyed',color=cq.Color(.38,.32,.24))
    assembly.add(cap,name='Cap_Schematic_75_Thick_50_Projection_Not_Measured',color=cq.Color(.65,.65,.61))
    path=out/'7111-chimney-01.step';assembly.export(str(path),'STEP')
    imported=cq.importers.importStep(str(path));assert len(imported.solids().vals())==2
    b=body.BoundingBox();c=cap.BoundingBox();bounds=lambda s:{'x':s.xlen,'y':s.ylen,'z':s.zlen}
    assert abs(b.xlen-p['base_x_mm'])<.001 and abs(b.ylen-p['base_y_mm'])<.001 and abs(b.zlen-p['brickwork_height_mm'])<.001
    assert abs(c.zmin-p['brickwork_height_mm'])<.001
    report={'units':'mm','body_envelope':bounds(b),'cap':bounds(c),'cap_status':'authorised schematic estimate','step_solids':len(imported.solids().vals()),'body_valid':body.isValid(),'cap_valid':cap.isValid(),'measured_masonry_volume_claimed':False}
    (out/'model-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    return p,body,cap

if __name__=='__main__':export()
