from EventQueue import EventQueue
from TreatmentEvent import TreatmentEvent
from AssessmentEvent import AssessmentEvent

class ArrivalEvent:
    def __init__(self, time, patient):
        self.time = time  # Time when the patient arrives
        self.patient = patient  # The patient object associated with this event
    
    def process(self, event_queue):
        # Determine the type of patient (emergency or walk-in) and log their arrival
        patient_type = 'Emergency' if self.patient.get_patient_type() == 'E' else 'Walk-In'
        print(f"Time {self.time}: {self.patient.get_patient_id()} ({patient_type}) arrives")
        
        if self.patient.get_patient_type() == 'E':
            # Emergency patients have a priority of 1
            self.patient.priority = 1
            print(f"Time {self.time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) enters waiting room")

            # Schedule treatment for the emergency patient after 1 time unit
            treatment_time = self.time + 1
            print(f"Time {self.time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) starts treatment (waited 0, 2 rm(s) remain)")
            event_queue.add_event(TreatmentEvent(treatment_time, self.patient))
        else:
            # Walk-in patients go through an assessment
            print(f"Time {self.time}: {self.patient.get_patient_id()} starts assessment (waited 0)")
            assessment_time = self.time + 4  # Assume assessment takes 4 time units
            event_queue.add_event(AssessmentEvent(assessment_time, self.patient))
