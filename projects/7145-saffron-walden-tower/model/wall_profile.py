"""Survey course-count wall offsets; unmeasured course pitch is visual only.
Three 150 mm outward steps at 20-course intervals in lower plinth; lowest return 300 mm.
The course pitch is a graphical proxy anchoring the plinth at first-floor level.
The nominal 650 mm shaft envelope closes 8000 external / 5200 clear with the given returns; engineer described first-floor thickness as approximately 550/600 mm.
"""
import math
PLINTH_TOP=5600.0+175.0
COURSE_PITCH=PLINTH_TOP/(4*20)
COURSES_PER_STEP=20
STEP_HEIGHT=COURSE_PITCH*COURSES_PER_STEP
BASE_EXTERNAL=8000.0
CLEAR_WIDTH=5200.0
BASE_WALL=(BASE_EXTERNAL-CLEAR_WIDTH)/2
TOP_ENVELOPE=BASE_WALL-(3*150.0+300.0)
OFFSET=150.0
BASE_RETURN=300.0
HEIGHT=25000.0

def segments(height=HEIGHT):
 # Three 150mm steps and the 300mm base return, confined to the lower plinth.
 # The shaft above the fourth 20-course band has a constant wall envelope.
 cuts=[0.]+[STEP_HEIGHT*i for i in range(1,5) if STEP_HEIGHT*i<height]+[float(height)]
 bands=[]
 for lo,hi in zip(cuts,cuts[1:]):
  if lo<STEP_HEIGHT:t=TOP_ENVELOPE+3*OFFSET+BASE_RETURN
  elif lo<2*STEP_HEIGHT:t=TOP_ENVELOPE+3*OFFSET
  elif lo<3*STEP_HEIGHT:t=TOP_ENVELOPE+2*OFFSET
  elif lo<4*STEP_HEIGHT:t=TOP_ENVELOPE+OFFSET
  else:t=TOP_ENVELOPE
  bands.append((lo,hi,t))
 return bands

def thickness(z):
 return next((t for lo,hi,t in segments() if lo<=z<hi),TOP_ENVELOPE)
