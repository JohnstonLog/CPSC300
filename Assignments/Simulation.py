from queue import PriorityQueue
from PatientClass import Patient
import Event 
import random

# create a hospital simulation object that contains a prio queue, 
class HospitalSimulation:
    def __init__(self):
        self.eventQueue = PriorityQueue() 
        self.time = 0
        self.patients = []
        self.treatment_rooms = 3

    def load_patients(self, file_path):
        with open(file_path, 'r') as file:
            id_num = 28064212
            for line in file:
                time, type_, treatment_time = line.split()
                patient_id = id_num
                id_num += 1
                patient = Patient(patient_id, int(time), type_, int(treatment_time))
                self.patients.append(patient)
                arrival_event = Event.ArrivalEvent(patient.arrival_time, patient)
                self.schedule_event(arrival_event)


    def initialize_simulation(self, file_path):
        self.load_patients(file_path)
        print("Simulation begins...")
        while not self.eventQueue.empty():
            self.process_next_event()

    #event processing methods

    def process_arrival_event(self, event):
        patient = event.patient
        print(f"Time {event.time}: {patient.patient_id} arrives")

        #walk in patients create assesment event 4 time units after the arrival
        if patient.patient_type == 'W':
            print(f"Time {event.time}: {patient.patient_id} starts assessment (implement wait time)")
            assessment_event = Event.AssessmentEvent(event.time + 4, patient)
            self.schedule_event(assessment_event)
        
        #emergency patients immediatly create an enter waiting room event
        else:
            ewr_event = Event.EnterWaitingRoomEvent(event.time, patient)
            self.schedule_event(ewr_event)


    def process_assessment_event(self, event):
        patient = event.patient
        patient.set_patient_priority() # set patients prio

        print(f"Time {event.time}: {patient.patient_id} assessment completed (priority now {patient.priority})")
        
        #create a new EWR event
        print(f"Time {event.time}: {patient.patient_id} (Priority {patient.priority}) enters waiting room")
        ewr_event = Event.EnterWaitingRoomEvent(event.time, patient)
        self.schedule_event(ewr_event)


    def process_ewr_event(self, event):
        patient = event.patient

        if self.treatment_rooms > 0:
            
            treatment_event = Event.StartTreatmentEvent(event.time, patient)
            self.schedule_event(treatment_event)
            self.treatment_rooms -= 1
            print(f"Time {event.time}: {patient.patient_id} (priority {patient.priority}) starts treatment (wait time #, {self.treatment_rooms} room(s) remain)")
        else:
            patient.wait_time += 1
            #...


    def process_start_treatment_event(self, event):
        patient = event.patient

        treatment_complete_event = Event.TreatmentCompleteEvent(event.time + patient.treatment_time, patient)
        self.schedule_event(treatment_complete_event)


    def process_treatment_complete_event(self, event):
        patient = event.patient
        self.treatment_rooms += 1

        if patient.priority == 1:
            admission_event = Event.AddmissionCompleteEvent(event.time +3, patient)
            self.schedule_event(admission_event)
        else:
            departure_event = Event.DepartureEvent(event.time, patient)
            self.schedule_event(departure_event)


    def process_admission_complete_event(self, event):
        patient = event.patient
        print(f"Time {event.time}: {patient.patient_id} admission complete")

    
    def process_departure_event(self, event):
        patient = event.patient
        print(f"Time {event.time}: {patient.patient_id} has departed")


    # schedule event method
    def schedule_event(self, event):
        self.eventQueue.put((event.time, event))

    #process next event method
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
        elif isinstance(next_event, Event.AddmissionCompleteEvent):
            self.process_admission_complete_event(next_event)

    