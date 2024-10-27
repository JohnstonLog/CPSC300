import random
from TreatmentEvent import TreatmentEvent

class AssessmentEvent:
    def __init__(self, time, patient):
        self.time = time  # The time when the assessment starts
        self.patient = patient  # The patient being assessed
    
    def process(self, event_queue):
        # Assign a random priority between 2 and 5 to the walk-in patient
        self.patient.priority = random.randint(2, 5)
        print(f"Time {self.time}: {self.patient.get_patient_id()} assessment completed (Priority now {self.patient.priority})")

        # Log that the patient enters the waiting room after assessment
        print(f"Time {self.time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) enters waiting room")

        # Schedule treatment for the patient to start after entering the waiting room
        treatment_time = self.time + 1
        event_queue.add_event(TreatmentEvent(treatment_time, self.patient))
