import random
from queue import PriorityQueue

# Patient constructor
class Patient:
    def __init__(self, patient_id, arrival_time, patient_type, treatment_time):
        self.patient_id = patient_id               # Patient ID (unique identifier)
        self.arrival_time = arrival_time           # Time the patient arrives at the hospital
        self.patient_type = patient_type           # 'E' for emergency, 'W' for walk-in
        self.treatment_time = treatment_time       # Duration of the treatment
        self.priority = None                       # To be determined after arrival or assessment

        # Time tracking attributes
        self.assessment_wait_time = 0
        self.assessment_queue_time = None
        self.assessment_time = None
        self.ewr_wait_time = 0
        self.ewr_queue_time = None  # Added this attribute
        self.departure_time = None
        self.admission_wait_time = 0
        self.admission_queue_time = None

    # Method to assign priority based on patient type (Emergency or Walk-in)
    def set_patient_priority(self):
        if self.patient_type == 'W' and self.priority is None:
            # Walk-in patients get a random priority between 2 and 5
            self.priority = random.randint(2, 5)
        elif self.patient_type == 'E' and self.priority is None:
            # Emergency patients always have the highest priority (1)
            self.priority = 1
