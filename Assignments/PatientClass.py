import random
from queue import PriorityQueue

random.seed(203)

#patient constructor
class Patient:
  def __init__(self, patient_id, arrival_time, patient_type, treatment_time):
    self.patient_id = patient_id                         # patient ID from global variable
    self.arrival_time = arrival_time                     # Read from file
    self.patient_type = patient_type                     # Read From file (E or W)
    self.treatment_time = treatment_time                 # Read from file
    self.priority = None                                 # determined after
    self.assessment_wait_time = 0
    self.assessment_time = 0                        
    self.ewr_wait_time = 0
    self.admission_wait_time = 0
    self.departure_time = 0


  def set_patient_priority(self):
    if self.patient_type == 'W' and self.priority is None:
      self.priority = random.randint(1, 5)
    elif self.patient_type == 'E' and self.priority is None:
      self.priority = 1