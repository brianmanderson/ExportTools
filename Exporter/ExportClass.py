from connect import *
from typing import Union
from RaystationInfoStructure.BaseStructure import *


class LoadPatientClass(object):
    def __init__(self, patient_db):
        self.patient_db = patient_db

    def load_patient_from_info(self, info):
        patient = self.patient_db.LoadPatient(PatientInfo=info, AllowPatientUpgrade=False)
        return patient

    def load_patient(self, rs_uid: str):
        info = self.patient_db.QueryPatientInfo(Filter={"Id": rs_uid}, UseIndexService=False)
        patient = self.patient_db.LoadPatient(PatientInfo=info[0], AllowPatientUpgrade=False)
        return patient


class ExportBaseClass(object):
    export_path: Union[str, bytes, os.PathLike]
    patient_loader: LoadPatientClass

    def __init__(self):
        self.patient_loader = LoadPatientClass(get_current("PatientDB"))
        self.rs_patient = None

    def set_export_path(self, path: Union[str, bytes, os.PathLike]):
        self.export_path = path

    def set_patient(self, patient: PatientClass):
        self.rs_patient = self.patient_loader.load_patient(patient.RS_UID)

    def export_all_in_patient(self, patient: PatientClass):
        self.set_patient(patient)
        self.export_examinations_and_structures(patient)
        self.export_dose(patient)

    def export_examinations(self, patient: PatientClass):
        for case in patient.Cases.values():
            rs_case = self.rs_patient.Cases[case.CaseName]
            for exam in case.Examinations.values():
                export_path = os.path.join(self.export_path, "Case_{}".format(case.Case_UID),
                                           "Exam_{}".format(exam.Exam_UID))
                if not os.path.exists(export_path):
                    os.makedirs(export_path)
                rs_case.ScriptableDicomExport(ExportFolderPath=export_path,
                                              Examinations=[exam.ExamName])

    def export_examinations_and_structures(self, patient: PatientClass):
        for case in patient.Cases.values():
            rs_case = self.rs_patient.Cases[case.CaseName]
            for exam in case.Examinations.values():
                export_path = os.path.join(self.export_path, "Case_{}".format(case.Case_UID),
                                           "Exam_{}".format(exam.Exam_UID))
                if not os.path.exists(export_path):
                    os.makedirs(export_path)
                rs_case.ScriptableDicomExport(ExportFolderPath=export_path,
                                              Examinations=[exam.ExamName],
                                              RtStructureSetsForExaminations=[exam.ExamName])

    def export_dose(self, patient: PatientClass):
        for case in patient.Cases.values():
            rs_case = self.rs_patient.Cases[case.CaseName]
            for treatment_plan in case.TreatmentPlans.values():
                plan_name = treatment_plan.PlanName
                for beam_set in treatment_plan.BeamSets.values():
                    beam_set_name = beam_set.DicomPlanLabel
                    export_path = os.path.join(self.export_path, "Case_{}".format(case.Case_UID),
                                               "Plan_{}".format(treatment_plan.TreatmentPlan_UID),
                                               "Beam_{}".format(beam_set.BeamSetUID))
                    if not os.path.exists(export_path):
                        os.makedirs(export_path)
                    rs_case.ScriptableDicomExport(ExportFolderPath=export_path,
                                                  BeamSetDoseForBeamSets=["%s:%s" % (plan_name, beam_set_name)])


if __name__ == '__main__':
    pass
