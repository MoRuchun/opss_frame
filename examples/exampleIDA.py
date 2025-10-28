"""
Performs incremental dynamic analysis using a single pair of records with 10 runs.

Note: for full IDA, a suite of records must be increased.
"""
from pathlib import Path
from rcmrf import RCMRF
import pickle

from utils.utils import get_time, get_start_time


start_time = get_start_time()

# Directories
main_dir = Path.cwd()
input_dir = main_dir / "Inputs"
materials_file = input_dir / "materials.csv"
outputsDir = main_dir / "outputs/ida"
loads_file = input_dir / "action.csv"

section_file = input_dir / "hinge_models.pickle"
with open(section_file, "rb") as f:
    section_file = pickle.load(f)

# GM directory
gmdir = main_dir / "gm_ida"

gmfileNames = ["GMR_names1.txt", "GMR_names2.txt", "GMR_dts.txt"]

# RCMRF inputs
hingeModel = "hysteretic"
system = "space"
analysis_type = ["IDA"]
flag3d = True
# Export outputs as a single file (this time :))
export_at_each_step = False
analysis_time_step = 0.01
max_runs = 10
periods_ida = [0.96, 1.03]
damping = 0.05

m = RCMRF(section_file, loads_file, materials_file, outputsDir, gmdir=gmdir, gmfileNames=gmfileNames,
          analysis_type=analysis_type, system=system, hinge_model=hingeModel, flag3d=flag3d,
          export_at_each_step=export_at_each_step, periods_ida=periods_ida, damping=damping,
          max_runs=max_runs, analysis_time_step=analysis_time_step)

m.wipe()
m.run_model()

# Wipe the model
m.wipe()

# Time it
get_time(start_time)
