from EventQueue import EventQueue
from TreatmentEvent import TreatmentEvent
from AssessmentEvent import AssessmentEvent

class ArrivalEvent:
    def __init__(self, time, patient):
        self.time = time
        self.patient = patient
    
    def process(self, event_queue):
        patient_type = 'Emergency' if self.patient.get_patient_type() == 'E' else 'Walk-In'
        print(f"Time {self.time}:  {self.patient.get_patient_id()} ({patient_type}) arrives")
        
        if self.patient.get_patient_type() == 'E':
            self.patient.priority = 1
            print(f"Time {self.time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) enters waiting room")
            treatment_time = self.time + 1
            print(f"Time {self.time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) starts treatment (waited 0, 2 rm(s) remain)")
            event_queue.add_event(TreatmentEvent(treatment_time, self.patient))
        else:
            print(f"Time {self.time}: {self.patient.get_patient_id()} starts assessment (waited 0)")
            assessment_time = self.time + 4
            event_queue.add_event(AssessmentEvent(assessment_time, self.patient))
