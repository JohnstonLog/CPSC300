from PatientClass import Patient
from queue import PriorityQueue

# change read patient data so that it creates an arrival event and immediatly pushes to event queue
def create_arrival_event(file_name):
    with open(file_name, 'r') as file:
        patient_id = 28064212
        wait_time = 0
        treatment_start_time = 0
        for line in file:
            # Reading the data form the file
            arrival_time, patient_type, treatment_time = line.split()
            arrival_time = int(arrival_time)
            treatment_time = int(treatment_time)
<<<<<<< HEAD

            # Create a new Patient object
            patient = Patient(patient_id, arrival_time, patient_type, treatment_time, wait_time, treatment_start_time) #"trear, typo corrected?"
            patients.append(patient)
=======
            # Create a Patient object
            patient = Patient(patient_id, arrival_time, patient_type, treatment_time, wait_time, treatment_start_time)
>>>>>>> b21a0ebb915a633519c7b2faefe2977cc6da4962
            patient_id += 1  # Increment patient number
    return arrival_event

#main body

event_queue = PriorityQueue() #initialize event queue

fileName = 'Assignments\\data3.txt'
patients = read_patient_data(fileName)

for patient in patients:
    print(patient.arrival_time, patient.patient_type)