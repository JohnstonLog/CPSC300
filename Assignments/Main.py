import Simulation
import PatientClass
import Event

sim = Simulation.HospitalSimulation()

file_path = input("Enter File Path: ")

sim.initialize_simulation(file_path)