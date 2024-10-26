from PatientClass import Patient

class ArrivalEvent:
    def __init__(self, Patient):
        self.time = Patient.arrival_time
        self.patient_type = Patient.patient_type
        self.priority = Patient.priority

    def check_priority(Patient):
        #set patient ID
        if Patient.priority = 1:
            #create enter wating room event
        else: 
            #create assesment event