from DepartureEvent import DepartureEvent

class TreatmentEvent:
    def __init__(self, time, patient):
        self.time = time  # Time when treatment starts
        self.patient = patient  # The patient receiving treatment

    def process(self, event_queue):
        # Log the start of treatment
        print(f"Time {self.time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) starts treatment")
        
        # Calculate the time when the treatment will be completed
        treatment_complete_time = self.time + self.patient.get_treatment_time()
        print(f"Time {treatment_complete_time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) finishes treatment")
        
        # After treatment finishes, handle based on patient priority
        if self.patient.priority == 1:
            # Priority 1 patients are admitted to the hospital after treatment
            print(f"Time {treatment_complete_time}: {self.patient.get_patient_id()} (Priority {self.patient.priority}) admitted to hospital")
            # Optionally, an AdmissionEvent could be scheduled here
        else:
            # Non-priority 1 patients leave after treatment
            print(f"Time {treatment_complete_time}: {self.patient.get_patient_id()} departs")
            # Schedule a DepartureEvent for the patient to leave
            event_queue.add_event(DepartureEvent(treatment_complete_time + 1, self.patient))
