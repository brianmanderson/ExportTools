# ExportTools

Utility for bulk-exporting DICOM data (image sets, RT structure sets, and beam-set dose) out of RayStation, driven by patient objects from the companion `InfoStructure` package. It runs inside the RayStation scripting environment and writes each patient's data into a folder tree organized by case, exam, plan, and beam-set UIDs.

Small single-module utility; last updated March 2024.

## How it works

`ExportClass.py` provides two classes:

- `LoadPatientClass` — looks up a patient in the RayStation `PatientDB` by MRN and loads it (no patient upgrade allowed).
- `ExportBaseClass` — given an export path and an `InfoStructure` `PatientClass`, calls RayStation's `ScriptableDicomExport` to write DICOM files:
  - `export_examinations(patient)` — image sets only, to `Case_{UID}/Exam_{UID}/`
  - `export_examinations_and_structures(patient)` — image sets plus their RT structure sets
  - `export_dose(patient)` — beam-set dose for every treatment plan, to `Case_{UID}/Plan_{UID}/Beam_{UID}/`
  - `export_all_in_patient(patient)` — examinations + structures, then dose

## Requirements

- RayStation scripting environment (`connect` module, `get_current("PatientDB")`)
- `InfoStructure` (private companion repo: patient/case/exam data model built from RayStation data)

## Usage

```python
exporter = ExportBaseClass()
exporter.set_export_path(r"\\path\to\export\folder")
exporter.export_all_in_patient(patient)  # patient: InfoStructure PatientClass
```
