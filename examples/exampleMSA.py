"""
Example application of MSA using 2 processors for parallel running of 2 intensity levels (return periods).
Each batch of record contains 3 pairs of records.

Note: this is a sample application that takes several minutes depending on the processors. For full fledged application
the record database should be more comprehensive and number of processors input may be removed to assign all available
processors.
"""

from pathlib import Path

from rcmrf import RCMRF
import pickle

import numpy as np

from utils.utils import get_time, get_start_time
from analysis.multiStripeAnalysis import MultiStripeAnalysis


if __name__ == "__main__":
    """Protect"""

    start_time = get_start_time()

    # Directories
    main_dir = Path.cwd()
    input_dir = main_dir / "Inputs"
    materials_file = input_dir / "materials.csv"
    outputsDir = main_dir / "outputs/msa"
    loads_file = input_dir / "action.csv"

    section_file = input_dir / "hinge_models.pickle"
    with open(section_file, "rb") as f:
        section_file = pickle.load(f)

    # GM directory
    gmdir = main_dir / "recordsMSA"

    # The naming convention must be the same for each intensity levels
    gmfileNames = ["GMR_H1_names.txt", "GMR_H2_names.txt", "GMR_dts.txt"]

    # RCMRF inputs
    hingeModel = "hysteretic"
    system = "space"
    analysis_type = ["MSA"]
    flag3d = True
    export_at_each_step = True
    analysis_time_step = 0.01
    periods_ida = [0.96, 1.03]
    damping = 0.05

    m = RCMRF(section_file, loads_file, materials_file, outputsDir, gmdir=gmdir,
              analysis_type=analysis_type, system=system, hinge_model=hingeModel, flag3d=flag3d,
              gmfileNames=gmfileNames, export_at_each_step=export_at_each_step,
              analysis_time_step=analysis_time_step, periods_ida=periods_ida, damping=damping)

    m.wipe()
    m.run_model()

    if "MSA" in analysis_type:
        omegas = 2 * np.pi / np.array(periods_ida)

        msa = MultiStripeAnalysis(section_file, loads_file, materials_file, gmdir, damping, omegas, outputsDir,
                                  system=system, hingeModel=hingeModel, flag3d=flag3d,
                                  export_at_each_step=export_at_each_step, pflag=True,
                                  analysis_time_step=analysis_time_step, drift_capacity=10.)

        msa.start_process(m.records, 1)

    # Wipe the model
    m.wipe()

    # Time it
    get_time(start_time)
