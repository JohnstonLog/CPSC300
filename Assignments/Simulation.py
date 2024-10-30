from queue import PriorityQueue, Queue
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
        self.assessment_queue = Queue()
        self.assessment_room_available = True

    def load_patients(self, file_path):
        with open(file_path, 'r') as file:
            id_num = 28064212
            for line in file:
                arrival_time, patient_type, treatment_time = line.split()
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

    #event processing methods

    def process_arrival_event(self, event):
        patient = event.patient
        print(f"Time {event.time}: {patient.patient_id} ({patient.patient_type}) arrives")

        #walk in patients create assesment event 4 time units after the arrival
        if patient.patient_type == 'W':
            #if there is no one already being assessed then create assessment event and schedule in event queue
            #and set the assessment room availability to false
            if self.assessment_room_available == True:
                print(f"Time {event.time}: {patient.patient_id} starts assessment (waited {patient.assessment_wait_time})")
                self.assessment_room_available = False
                assessment_event = Event.AssessmentEvent(event.time + 4, patient)
                self.schedule_event(assessment_event)
            else:
                # the time of this event will be the time that they started waiting
                assessment_event = Event.AssessmentEvent(event.time, patient)
                self.assessment_queue.put(assessment_event)
            
        
        #emergency patients immediatly create an enter waiting room event
        else:
            patient.set_patient_priority()
            ewr_event = Event.EnterWaitingRoomEvent(event.time, patient)
            self.schedule_event(ewr_event)


    def process_assessment_event(self, event):
        patient = event.patient
        patient.set_patient_priority() # set patients prio
        print(f"Time {event.time}: {patient.patient_id} assessment completed (priority now {patient.priority})")

        self.assessment_room_available = True # make assessment room available again

        #create a new EWR event
        print(f"Time {event.time}: {patient.patient_id} (Priority {patient.priority}) enters waiting room")
        ewr_event = Event.EnterWaitingRoomEvent(event.time, patient)
        self.schedule_event(ewr_event)

        # if there is someone waiting to be assessed we take them from the queue and create an assessment event for them
        if not self.assessment_queue.empty():
            next_event = self.assessment_queue.get()
            next_patient = next_event.patient
            next_patient.assessment_wait_time = event.time - next_event.time
            print(f"Time {event.time}: {next_patient.patient_id} starts assessment (waited {next_patient.assessment_wait_time})")
            self.assessment_room_available = False
            next_assessment_event = Event.AssessmentEvent(next_event.time + 4, next_patient)
            self.schedule_event(next_assessment_event)


    def process_ewr_event(self, event):
        patient = event.patient

        if self.treatment_rooms > 0:

            treatment_event = Event.StartTreatmentEvent(event.time, patient)
            self.schedule_event(treatment_event)
            self.treatment_rooms -= 1
            print(f"Time {event.time}: {patient.patient_id} (priority {patient.priority}) starts treatment (waited {patient.ewr_wait_time}, {self.treatment_rooms} room(s) remain)")
        else:
            patient.ewr_wait_time += 1
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

    