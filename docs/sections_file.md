# Creating a section information file

The NLTHA workflows in `opss_frame` expect a *section information file* (the `sections_file` argument) that fully describes the lumped plastic hinge properties for every beam and column in the model. This guide explains the required columns and presents two supported workflows for generating the file.

## Required columns

The `client.Model` class loads the section information file and expects the following fields for each element: `Element`, `Bay`, `Storey`, `Position`, `b`, `h`, `cover`, `Pgrav`, `Plateral`, `MyPos`, `MyNeg`, `asl`, `Ash`, `spacing`, `db`, `c`, `D`, `Res`, `Length`, and `ro_long` (for 3D models, add a `Direction` column). Each numeric field should be stored as a floating-point value when the file is read by pandas.

If you are assembling the data manually, start from the sample CSV `examples/Inputs/hinge_models_hyst.csv` to confirm column names and units.

## Workflow A: Generate hinges with the Eurocode design helper

The Eurocode design pipeline produces hinge properties that are already compatible with NLTHA analyses. Use it when you want section properties derived from Eurocode-compliant gravity and seismic design checks.

1. Pick the input template that matches your structure (`design/model1.Input`, `design/model2.Input`, or create your own class mirroring the same attributes for storey heights, bay widths, loads, and material strengths).
2. Instantiate `EurocodeDesign` with the project name, site name, and dimensionality flag (`flag3d`) and call `get_design_gravity_loads()` to assemble factored loads.
3. Provide a site hazard file and preliminary member sizing (see the sample paths in `design/run_ec_design.py`) and run `run_modal_analysis()` followed by `apply_ec_based_analysis()` to obtain hinge models for each direction.
4. Persist the hinge models you need by toggling the `store` flag and exporting the desired direction to CSV via `utils.export_to` (uncomment or extend the sample export lines as needed). The resulting file can be passed directly as `sections_file` when running IDA or MSA.

## Workflow B: Build the file manually in pandas

1. Create a pandas `DataFrame` with one row per beam or column and populate every required column listed above. Ensure the element tags (`Element`, `Bay`, `Storey`, `Position`, and optional `Direction`) match the geometry definition that will be read by `client.Geometry`.
2. Cast the numeric columns to floats so that `Model` does not need to coerce the data at runtime.
3. Save the `DataFrame` as CSV or pickle (NLTHA notebooks accept both) and reference the path when instantiating `rcmrf.RCMRF` or `analysis` classes. A lightweight example is distributed at `examples/Inputs/hinge_models_hyst.csv`.

## Quality checks before running NLTHA

* Verify that the gravity and lateral axial forces (`Pgrav`, `Plateral`) reflect the combinations used during hinge calibration.
* Confirm that beam and column lengths match the story heights and bay widths given to the geometry builder.
* For 3D models, ensure both `x` and `y` seismic hinge tables are supplied (the keys will be normalized to `"x"` and `"y"` internally).

Following these steps will give you a well-formed section information file that the NLTHA workflows can consume without further adjustments.
