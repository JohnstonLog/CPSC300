class DepartureEvent:
    def __init__(self, time, patient):
        self.time = time  # The time when the patient departs
        self.patient = patient  # The patient who is leaving the hospital

    def process(self, event_queue):
        # Calculate total waiting time, treatment time, and time spent in the hospital
        waiting_time = self.patient.get_treatment_start_time() - self.patient.get_arrival_time()
        total_time_in_hospital = self.time - self.patient.get_arrival_time()
        treatment_time = self.patient.get_treatment_time()

        # Log the patient's departure with all relevant details
        print(f"Time {self.time}: {self.patient.get_patient_id()} departs")
        print(f"Patient {self.patient.get_patient_id()} spent {total_time_in_hospital} time units in the hospital.")
        print(f"Patient {self.patient.get_patient_id()} waited {waiting_time} time units before treatment.")
        print(f"Patient {self.patient.get_patient_id()} required {treatment_time} time units for treatment.")
