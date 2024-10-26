import PatientClass as Patient
from queue import PriorityQueue

def read_patient_data(file_name):
    patients = []
    with open(file_name, 'r') as file:
        patient_id = 28064212
        wait_time = 0
        treatment_start_time = 0
        for line in file:
            arrival_time, patient_type, treatment_time = line.split()
            treatment_time = int(treatment_time)
            # Create a Patient object
            patient = Patient(patient_id, arrival_time, patient_type, treatment_time, wait_time, trear=treatment_start_time)
            patients.append(patient)
            patient_id += 1  # Increment patient number
    return patients