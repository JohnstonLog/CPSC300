import random
from queue import PriorityQueue
#patient constructor
class Patient:
  def __init__(self, patient_id, arrival_time, patient_type, treatment_time):
    self.patient_id = patient_id                         # patient ID from global variable
    self.arrival_time = arrival_time                     # Read from file
    self.patient_type = patient_type                     # Read From file (E or W)
    self.treatment_time = treatment_time                 # Read from file
    self.priority = None                                 # Priority 1 if type E else random 1-5
    self.wait_time = None                                   # starts at 0


  def set_patient_priority(self):
    if self.patient_type == 'W' and self.priority is None:
      self.priority = random.randint(1, 5)
  

  
