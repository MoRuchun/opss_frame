<h1 align="center">Generic RC MRF model creator</h1>

Procedures to create a reinforced concrete building (3D), or a frame (2D) nonlinear building model
consisting of moment resisting frames (MRF) as the primary lateral load resisting system.

May use multiprocessing to carry out multiple stripe analysis (non-linear time history analyses).

May be used in any os system.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5753463.svg)](https://doi.org/10.5281/zenodo.5753463)

**Required libraries**: requirements.txt

      python -m pip install -r requirements.txt

### Table of Contents
<details open>
<summary>Show/Hide</summary>
<br>

1. [Supported analysis types](#analysis)
2. [Required input arguments](#input)
3. [Samples](#samples)

</details>


### Supported analysis types
<details>
<a name="analysis"></a>
<summary>Show/Hide</summary>
<br>

1. Non-linear time history analysis (NLTHA)
   1. Incremental dynamic analysis (IDA)
   2. Multiple stripe analysis (MSA)
	
</details>


### Required input arguments per analysis
<details>
<a name="input"></a>
<summary>Show/Hide</summary>
<br>

* **sections_file**

                CSV, pickle or DataFrame describing hysteretic model parameters. See
                [Creating a section information file](docs/sections_file.md) for
                the required columns and generation workflows.

* **loads_file**

                CSV file defining masses and gravity loads.

* **materials_file**

                CSV file containing material properties.

* **outputsDir**

                Directory to export analysis outputs.

* **gmdir**

                Directory containing ground motion records.

* **gmfileNames**

                Filenames describing ["GM_names_x", "GM_names_y", "GM_time_step"].

* **analysis_type**

                List or string identifying the workflows to run. Supported values: "IDA", "MSA".

* **periods_ida**

                List of periods used to scale and interpret ground motions. Required for IDA and for
                MSA when modal frequencies are not provided separately.

* **damping**

                Modal damping ratio (e.g. 0.05) used in nonlinear time history analyses.

* **IM_type**

                Intensity measure type for IDA (default 2 for Sa(T1)).

* **max_runs**

                Maximum number of runs per record for IDA (default 15).

* **analysis_time_step**

                Nonlinear analysis time step (default 0.01 s).

* **drift_capacity**

                Drift capacity threshold (%) to stop IDA (default 10).

* **system**

                Structural system description ("perimeter" or "space", default "space").

* **hinge_model**

                Lumped hinge model type ("hysteretic" or "haselton", default "hysteretic").

* **flag3d**

                False for 2D modelling, True for 3D modelling.

* **direction**

                Seismic loading direction for 3D analyses (0 for X, 1 for Y). Ignored for 2D models.

* **export_at_each_step**

                Export recorder outputs after each run (default True).

	
</details>


### Examples
<details>
<a name="samples"></a>
<summary>Show/Hide</summary>
<br>

**Non-linear time history workflows**

Example 1: IDA - exampleIDA.py

Example 2: MSA - exampleMSA.py


</details>

### Future
<details>
<a name="future"></a>
<summary>Show/Hide</summary>
<br>

* [ ] Quality testing
* [ ] Haselton hinge models, example
* [x] 2D application examples
* [ ] Elastic models
* [x] 3D application examples
* [ ] Update solutionAlgorithm to incorporate interpolation functions (secondary analysis option, not recommended)


</details>
