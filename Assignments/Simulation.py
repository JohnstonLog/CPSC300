from queue import PriorityQueue

# create a hospital simulation object that contains a prio queue, 
class HospitalSimulation:
    def __inti__(self):
        self.eventQueue = PriorityQueue() 
        self.time = 0
        self.patients = []
        self.treatment_rooms = 3

    

    #event processing methods
    def process_arrival_event(self, event):
        
    def process_assessment_event(self, event):

    def process_ewr_event(self, event):

    def process_start_treatment_event(self, event):

    def process_end_treatment_event(self, event):

    def process_admission_complete_event(self, event):

    # schedule event method
    def schedule_event(self, event):
        self.eventQueue.put((event.time, event))

    #process next event method
    def process_next_event(self):
        next_event = self.eventQueue.get()

        if isinstance(next_event, ArrivalEvent):
            self.process_arrival_event(next_event)
        elif isinstance(next_event, AssessmentEvent):
            self.process_assessment_event(next_event)
        elif isinstance(next_event, EnterWaitingRoomEvent):
            self.process_ewr_event(next_event)
        elif isinstance(next_event, StartTreatmentEvent):
            self.process_start_treatment_event(next_event)
        elif isinstance(next_event, TreatmentCompleteEvent):
            self.process_end_treatment_event(next_event)
        elif isinstance(next_event, AdmissionCompleteEvent):
            self.process_admission_complete_event(next_event)