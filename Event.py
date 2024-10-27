class Event:
    def __init__(self, time, patient, event_type):
        self.time = time
        self.patient = patient
        self.event_type = event_type
    
    # used to set the priority of attributes (ordered by time, then patient priority, then patient id)
    def __lt__(self, other):
        return(self.time, self.patient.priority, self.patient_id) < (other.time, other.patient.priority, other.patient_id)

# the following are sub classes that inherit the above class attributes (order)
# used to distinguish between different even types
class ArrivalEvent(Event): pass
class AssesmentEvent(Event): pass
class EnterWaitingRoomEvent(Event): pass
class StartTreatmentEvent(Event): pass
class TreatmentCompleteEvent(Event): pass
class AddmissionCompleteEvent(Event): pass