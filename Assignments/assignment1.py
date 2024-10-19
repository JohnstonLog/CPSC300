import random
from queue import PriorityQueue
#patient constructor
class Patient:
  def __init__(self, patient_id, arrival_time, patient_type, treatment_time, wait_time, treatment_start_time):
    self.patient_id = patient_id                         # patient ID from global variable
    self.arrival_time = arrival_time                     # Read from file
    self.patient_type = patient_type                     # Read From file
    self.treatment_time = treatment_time                 # Read from file
    self.priority = random.randint(1, 5)                 # From random
    self.wait_time = wait_time                           # calculated later
    self.treatment_start_time = treatment_start_time     # determined later

Patient1 = Patient