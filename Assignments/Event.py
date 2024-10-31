class Event:
    def __init__(self, time, patient):
        self.time = time
        self.patient = patient
    
    # used to set the priority of attributes (ordered by time, then patient priority, then patient id)
    def __lt__(self, other):
        # Assign a high value (e.g., 6) to None priorities to rank them as the lowest priority
        self_priority = self.patient.priority if self.patient.priority is not None else 6
        other_priority = other.patient.priority if other.patient.priority is not None else 6
        return (self.time, self_priority, self.patient.patient_id) < (other.time, other_priority, other.patient.patient_id)

# Subclasses inheriting from Event, used to distinguish between different event types
class ArrivalEvent(Event): pass
class AssessmentEvent(Event): pass
class EnterWaitingRoomEvent(Event): pass
class StartTreatmentEvent(Event): pass
class TreatmentCompleteEvent(Event): pass
class AdmissionCompleteEvent(Event): pass
class DepartureEvent(Event): pass
