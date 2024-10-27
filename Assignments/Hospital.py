from PatientClass import Patient
from ArrivalEvent import ArrivalEvent
from EventQueue import EventQueue

# Function to read patient data and create arrival events, and push them to the event queue
def create_arrival_event(file_name, event_queue):
    patients = []  # Initialize list to store patient objects
    with open(file_name, 'r') as file:
        patient_id = 28064212  # Starting patient ID
        wait_time = 0  # Initialize wait_time
        treatment_start_time = 0  # Initialize treatment_start_time
        for line in file:
            # Reading the data from the file
            arrival_time, patient_type, treatment_time = line.split()
            arrival_time = int(arrival_time)
            treatment_time = int(treatment_time)

            # Create a Patient object
            patient = Patient(patient_id, arrival_time, patient_type, treatment_time, wait_time, treatment_start_time)
            patients.append(patient)  # Add patient to the list

            # Create an ArrivalEvent and push it to the event queue
            arrival_event = ArrivalEvent(arrival_time, patient)
            event_queue.add_event(arrival_event)

            patient_id += 1  # Increment patient number
    return patients  # Return the list of patients for further use if needed

# Main body

event_queue = EventQueue()  # Initialize the custom EventQueue

file_name = 'Assignments\\data3.txt'
patients = create_arrival_event(file_name, event_queue)  # Read the data and create arrival events

# Print patient information for confirmation
for patient in patients:
    print(f"Patient ID: {patient.get_patient_id()}, Arrival Time: {patient.get_arrival_time()}, Type: {patient.get_patient_type()}")

# Process all events in the event queue
event_queue.process_events()
