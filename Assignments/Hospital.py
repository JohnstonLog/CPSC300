import PatientClass as Patient
from queue import PriorityQueue

def read_patient_data(file_name):
    patients = []
    with open(file_name, 'r') as file:
        patient_id = 28064212
        wait_time = 0
        treatment_start_time = 0
        for line in file:
            # Reading the data form the file
            arrival_time, patient_type, treatment_time = line.split()
            arrival_time = int(arrival_time)
            treatment_time = int(treatment_time)

            # Create a new Patient object
            patient = Patient(patient_id, arrival_time, patient_type, treatment_time, wait_time, treatment_start_time) #"trear, typo corrected?"
            patients.append(patient)
            patient_id += 1  # Increment patient number
    return patients