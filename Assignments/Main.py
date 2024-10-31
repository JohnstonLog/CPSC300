import Simulation

sim = Simulation.HospitalSimulation()

file_path = 'D:\cpsc300_a1\CPSC300\Assignments\data1.txt'

try:
    sim.initialize_simulation(file_path)
except Exception as e:
    print(f"An error occurred during simulation: {e}")
