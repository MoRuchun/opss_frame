"""Master interface for nonlinear time history analyses.

This module only retains the functionality required for incremental dynamic
analysis (IDA) and multiple stripe analysis (MSA). All other analysis types and
legacy orchestration logic have been removed in favour of a focused
non-linear time history workflow.
"""
import openseespy.opensees as op

from analysis.multiStripeAnalysis import get_records
from client.model import Model
import numpy as np
import os
import pickle
from analysis.ida_htf_3d import IDA_HTF_3D
from utils.utils import createFolder


class RCMRF:
    def __init__(self, sections_file, loads_file, materials_file, outputsDir, gmdir=None, gmfileNames=None, IM_type=2,
                 max_runs=15, analysis_time_step=None, drift_capacity=10., analysis_type=None, system="Space",
                 hinge_model="Hysteretic", flag3d=False, direction=0, export_at_each_step=True,
                 periods_ida=None, damping=0.05, use_recorder=True, recorder_cache=None):
        """
        Initializes the non-linear analysis orchestrator.

        Parameters
        ----------
        sections_file : str or dict
            Section definition(s) passed to :class:`client.model.Model`.
        loads_file : str
            CSV file describing gravity loads and masses.
        materials_file : str
            Concrete and reinforcement material properties.
        outputsDir : Path-like
            Directory for exporting analysis results.
        gmdir : Path-like, optional
            Directory containing ground motion files.
        gmfileNames : list[str], optional
            Filenames defining ground motion records and their metadata.
        IM_type : int, optional
            Intensity measure tag for IDA. Defaults to Sa(T1).
        max_runs : int, optional
            Maximum number of IDA runs.
        analysis_time_step : float, optional
            Integration time step for the transient analysis.
        drift_capacity : float, optional
            Drift capacity (in %) used to halt analyses.
        analysis_type : str or list[str], optional
            Combination of "IDA" and/or "MSA" indicating which workflows to run.
        system : str, optional
            Structural system description passed to :class:`client.model.Model`.
        hinge_model : str, optional
            Lumped hinge model type.
        flag3d : bool, optional
            Toggle between 2D and 3D modelling.
        direction : int, optional
            Seismic loading direction (0: x, 1: y) for 3D models.
        export_at_each_step : bool, optional
            Export IDA results after each record.
        periods_ida : list[float], optional
            Fundamental periods used to scale records. Required when running IDA.
        damping : float, optional
            Modal damping ratio used for NLTHA.
        use_recorder : bool, optional
            Use OpenSeesPy recorder outputs instead of node recorders.
        recorder_cache : str, optional
            Cache filename for acceleration recorders.
        """
        # list of strings for 3D modelling, and string for 2D modelling
        self.sections_file = sections_file

        # Input arguments
        self.outputsDir = outputsDir
        self.loads_file = loads_file
        self.materials_file = materials_file
        self.gmdir = gmdir
        self.gmfileNames = gmfileNames
        self.IM_type = IM_type
        self.max_runs = max_runs
        self.analysis_time_step = analysis_time_step
        self.drift_capacity = drift_capacity
        self.analysis_type = analysis_type
        self.system = system
        self.hinge_model = hinge_model.lower()
        self.flag3d = flag3d
        self.export_at_each_step = export_at_each_step
        self.direction = direction
        self.periods_ida = periods_ida
        self.damping = damping
        self.use_recorder = use_recorder
        self.recorder_cache = recorder_cache

        # Constants
        self.FIRST_INT = .05
        self.INCR_STEP = .05
        self.DAMPING = damping

        self.records = None

        # Create an outputs directory if none exists
        createFolder(outputsDir)

    @staticmethod
    def wipe():
        """
        Perform a clean wipe
        :return: None
        """
        op.wipe()

    def call_model(self, generate_model=True):
        """
        Calls the Model
        :param generate_model: bool                         Generate model or not
        :return: class                                      Object Model
        """
        m = Model(self.analysis_type, self.sections_file, self.loads_file, self.materials_file,
                  self.outputsDir, self.system, hingeModel=self.hinge_model, flag3d=self.flag3d,
                  direction=self.direction)

        if generate_model:
            m.model()

        return m

    def run_model(self):
        """
        Run the requested nonlinear time history workflows.
        """
        tags = self.analysis_type
        if tags is None:
            tags = []
        elif isinstance(tags, str):
            tags = [tags]

        allowed = {"IDA", "MSA"}
        unknown = [tag for tag in tags if tag not in allowed]
        if unknown:
            raise ValueError(f"Unsupported analysis types requested: {unknown}. Only 'IDA' and 'MSA' are available.")

        if "IDA" in tags:
            if self.periods_ida is None:
                raise ValueError("IDA requested but 'periods_ida' was not provided.")

            createFolder(self.outputsDir / "NLTHA")
            print("[INITIATE] IDA started")

            omegas = 2 * np.pi / np.array(self.periods_ida)

            ida = IDA_HTF_3D(self.FIRST_INT, self.INCR_STEP, self.max_runs, self.IM_type, self.periods_ida,
                             self.DAMPING, omegas, self.analysis_time_step, self.drift_capacity, self.gmdir,
                             self.gmfileNames, self.analysis_type, self.sections_file, self.loads_file,
                             self.materials_file, self.system, hingeModel=self.hinge_model, pflag=True,
                             flag3d=self.flag3d, export_at_each_step=self.export_at_each_step,
                             use_recorder=self.use_recorder, recorder_cache=self.recorder_cache)

            ida.establish_im(output_dir=self.outputsDir / "NLTHA")

            if not self.export_at_each_step:
                with open(self.outputsDir / "IDA.pickle", "wb") as handle:
                    pickle.dump(ida.outputs, handle)

            if os.path.exists(self.outputsDir / "IM.csv"):
                im_filename = "IM_temp.csv"
            else:
                im_filename = "IM.csv"
            np.savetxt(self.outputsDir / im_filename, ida.IM_output, delimiter=',')

            print("[SUCCESS] IDA done")

        if "MSA" in tags:
            createFolder(self.outputsDir / "MSA")
            print("[INITIATE] MSA started")
            self.records = get_records(self.gmdir, self.outputsDir / "MSA", self.gmfileNames)
            print("[SUCCESS] MSA setup complete")

