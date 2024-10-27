<<<<<<< HEAD
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
=======
from PatientClass import Patient

class ArrivalEvent:
    def __init__(self, Patient):
        self.time = Patient.arrival_time
        self.patient_type = Patient.patient_type
        self.priority = Patient.priority

    def check_priority(Patient):
        #set patient ID
        if Patient.priority = 1:
            #create enter wating room event
        else: 
            #create assesment event
>>>>>>> b21a0ebb915a633519c7b2faefe2977cc6da4962
