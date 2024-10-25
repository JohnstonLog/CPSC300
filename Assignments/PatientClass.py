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


  
  # getters and setters for patient class
  def set_patient_id(self, value):
    self.patient_id = value

  def get_patient_id(self):
    return self.patient_id

  def set_arrival_time(self, time):
    self.arrival_time = time

  def get_arrival_time(self):
    return self.arrival_time
  
  def set_patient_type(self, type):
    self.patient_type = type

  def get_patient_type(self):
    return self.patient_type
  
  def set_treatment_time(self, time):
    self.treatment_time = time

  def get_treatment_time(self):
    return self.treatment_time
  
  def set_wait_time(self, time):
    self.wait_time = time

  def get_wait_time(self):
    return self.wait_time
  
  def set_treatment_start_time(self, time):
    self.treatment_start_time = time

  def get_treatment_start_time(self):
    return self.treatment_start_time
  

  
