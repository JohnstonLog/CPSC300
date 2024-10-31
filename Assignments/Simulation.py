from queue import PriorityQueue, Queue
from PatientClass import Patient
import Event
import random

class HospitalSimulation:
    def __init__(self):
        self.eventQueue = PriorityQueue()
        self.time = 0
        self.patients = []
        self.treatment_rooms = 3
        self.assessment_queue = Queue()
        self.assessment_room_available = True
        self.ewr_queue = PriorityQueue()
        self.admission_queue = Queue()
        self.admission_nurse_available = True

    def load_patients(self, file_path):
        with open(file_path, 'r') as file:
            id_num = 28064212
            for line in file:
                arrival_time, patient_type, treatment_time = line.strip().split()
                patient_id = id_num
                id_num += 1
                patient = Patient(patient_id, int(arrival_time), patient_type, int(treatment_time))
                self.patients.append(patient)
                arrival_event = Event.ArrivalEvent(patient.arrival_time, patient)
                self.schedule_event(arrival_event)

    def initialize_simulation(self, file_path):
        self.load_patients(file_path)
        print("Simulation begins...")

        while not self.eventQueue.empty():
            self.process_next_event()

        print("... All events complete. Final Summary:")

        # Call functions to display the results and summary separately
        try:
            self.print_patient_data()
        except Exception as e:
            print(f"An error occurred in print_patient_data: {e}")

        try:
            self.print_summary()
        except Exception as e:
            print(f"An error occurred in print_summary: {e}")


    def process_arrival_event(self, event):
        patient = event.patient
        print(f"Time {event.time}: {patient.patient_id} ({patient.patient_type}) arrives")

        if patient.patient_type == 'W':
            if self.assessment_room_available:
                patient.assessment_wait_time = 0  # No waiting time
                print(f"Time {event.time}: {patient.patient_id} starts assessment (waited {patient.assessment_wait_time})")
                self.assessment_room_available = False  # Assessment room is now occupied
                patient.assessment_start_time = event.time  # Record assessment start time
                assessment_event = Event.AssessmentEvent(event.time + 4, patient)
                self.schedule_event(assessment_event)
            else:
                patient.assessment_queue_time = event.time  # Record when the patient started waiting
                self.assessment_queue.put(patient)
        else:
            # Emergency patients go directly to the waiting room
            patient.set_patient_priority()
            ewr_event = Event.EnterWaitingRoomEvent(event.time, patient)
            self.schedule_event(ewr_event)


    def process_assessment_event(self, event):
        patient = event.patient
        patient.set_patient_priority()  # Set patient's priority after assessment
        patient.assessment_end_time = event.time  # Record the assessment completion time

        print(f"Time {event.time}: {patient.patient_id} assessment completed (priority now {patient.priority})")

        self.assessment_room_available = True

        ewr_event = Event.EnterWaitingRoomEvent(event.time, patient)
        self.schedule_event(ewr_event)

        # If there is another patient waiting for assessment, start their assessment
        if not self.assessment_queue.empty():
            next_patient = self.assessment_queue.get()
            next_patient.assessment_wait_time = event.time - next_patient.assessment_queue_time  # Calculate wait time
            print(f"Time {event.time}: {next_patient.patient_id} starts assessment (waited {next_patient.assessment_wait_time})")
            self.assessment_room_available = False  # Assessment room is now occupied
            next_patient.assessment_start_time = event.time  # Record assessment start time
            next_assessment_event = Event.AssessmentEvent(event.time + 4, next_patient)
            self.schedule_event(next_assessment_event)


    def process_ewr_event(self, event):
        patient = event.patient

        if self.treatment_rooms > 0:
            print(f"Time {event.time}: {patient.patient_id} (Priority {patient.priority}) goes directly to treatment")
            start_treatment_event = Event.StartTreatmentEvent(event.time, patient)
            self.schedule_event(start_treatment_event)
        else:
            # Record when the patient started waiting in the emergency waiting room
            patient.ewr_queue_time = event.time
            # Include arrival time as a tie-breaker
            self.ewr_queue.put((patient.priority, patient.arrival_time, patient))
            print(f"Time {event.time}: {patient.patient_id} (Priority {patient.priority}) added to emergency waiting room")


    def process_start_treatment_event(self, event):
        patient = event.patient
        self.treatment_rooms -= 1  # Decrease number of available treatment rooms
        if hasattr(patient, 'ewr_queue_time') and patient.ewr_queue_time is not None:
            patient.ewr_wait_time = event.time - patient.ewr_queue_time  # Calculate wait time
        else:
            patient.ewr_wait_time = event.time - patient.arrival_time  # For patients who didn't wait in EWR
        print(f"Time {event.time}: {patient.patient_id} (Priority {patient.priority}) starts treatment "
              f"(waited {patient.ewr_wait_time}, {self.treatment_rooms} rm(s) remain)")
        treatment_complete_event = Event.TreatmentCompleteEvent(event.time + patient.treatment_time, patient)
        self.schedule_event(treatment_complete_event)

    def process_treatment_complete_event(self, event):
        patient = event.patient
        print(f"Time {event.time}: {patient.patient_id} finished treatment")

        self.treatment_rooms += 1  # Free up treatment room

        if patient.priority == 1:
            if self.admission_nurse_available:
                self.admission_nurse_available = False  # Nurse is now busy
                patient.admission_wait_time = 0
                admission_event = Event.AdmissionCompleteEvent(event.time + 3, patient)
                self.schedule_event(admission_event)
            else:
                # Nurse is busy; add patient to the admission queue
                patient.admission_queue_time = event.time  # Record when patient started waiting
                self.admission_queue.put(patient)
        else:
            departure_event = Event.DepartureEvent(event.time + 1, patient)
            self.schedule_event(departure_event)

        # After freeing up the treatment room, check if any patients are waiting
        while self.treatment_rooms > 0 and not self.ewr_queue.empty():
            next_patient_tuple = self.ewr_queue.get()
            next_patient = next_patient_tuple[2]
            start_treatment_event = Event.StartTreatmentEvent(event.time, next_patient)
            self.schedule_event(start_treatment_event)
            # The treatment room will be decremented in process_start_treatment_event when treatment starts

    def process_admission_complete_event(self, event):
        patient = event.patient
        print(f"Time {event.time}: {patient.patient_id} (priority {patient.priority}, waited {patient.admission_wait_time}) admitted to Hospital")
        departure_event = Event.DepartureEvent(event.time, patient)
        self.schedule_event(departure_event)
        self.admission_nurse_available = True

        # If someone is waiting in the admission queue, start their admission
        if not self.admission_queue.empty():
            next_patient = self.admission_queue.get()
            next_patient.admission_wait_time = event.time - next_patient.admission_queue_time
            self.admission_nurse_available = False  # Nurse is now busy
            next_admission_event = Event.AdmissionCompleteEvent(event.time + 3, next_patient)
            self.schedule_event(next_admission_event)

    def process_departure_event(self, event):
        patient = event.patient
        patient.departure_time = event.time  # Record the departure time for the patient

        # Log the patient's departure
        print(f"Time {event.time}: {patient.patient_id} departs")

    # Schedule event method
    def schedule_event(self, event):
        self.eventQueue.put((event.time, event))

    # Process next event method
    def process_next_event(self):
        next_event = self.eventQueue.get()[1]

        if isinstance(next_event, Event.ArrivalEvent):
            self.process_arrival_event(next_event)
        elif isinstance(next_event, Event.AssessmentEvent):
            self.process_assessment_event(next_event)
        elif isinstance(next_event, Event.EnterWaitingRoomEvent):
            self.process_ewr_event(next_event)
        elif isinstance(next_event, Event.StartTreatmentEvent):
            self.process_start_treatment_event(next_event)
        elif isinstance(next_event, Event.TreatmentCompleteEvent):
            self.process_treatment_complete_event(next_event)
        elif isinstance(next_event, Event.AdmissionCompleteEvent):
            self.process_admission_complete_event(next_event)
        elif isinstance(next_event, Event.DepartureEvent):
            self.process_departure_event(next_event)

    def print_patient_data(self):
        print(f"{'Patient':<10} {'Priority':<10} {'Arrival':<10} {'Assessment':<15} {'Treatment':<12} {'Departure':<12} {'Waiting':<10}")
        print('-' * 80)

        for patient in self.patients:
            patient_id = patient.patient_id
            priority = patient.priority if patient.priority is not None else 'N/A'
            arrival_time = patient.arrival_time

            # For emergency patients, assessment_start_time will be None; use arrival_time instead
            assessment_time = patient.assessment_start_time if patient.assessment_start_time is not None else patient.arrival_time

            treatment_time = patient.treatment_time
            departure_time = patient.departure_time if patient.departure_time is not None else 'N/A'
            waiting_time = patient.ewr_wait_time if patient.ewr_wait_time is not None else 0

            # Print the formatted patient information
            print(f"{patient_id:<10} {priority:<10} {arrival_time:<10} {assessment_time:<15} {treatment_time:<12} {departure_time:<12} {waiting_time:<10}")



    def print_summary(self):
        total_waiting_time = 0
        total_patients = len(self.patients)

        for patient in self.patients:
            total_waiting_time += patient.ewr_wait_time if patient.ewr_wait_time is not None else 0

        avg_waiting_time = total_waiting_time / total_patients if total_patients > 0 else 0

        print(f"\nPatients seen in total: {total_patients}")
        print(f"Average waiting time per patient: {avg_waiting_time:.6f}")
