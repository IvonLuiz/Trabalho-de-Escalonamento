from system import System
from algorithms.fifo import Fifo
from algorithms.sjf import SJF
from algorithms.edf import EDF
from csv_reader import CSVReader

CSV_FILE = 'csv/input_file.csv'
processes = CSVReader(CSV_FILE).get_processes()

system = System(processes, overhead=0, quantum=2)

# system.add_process(0, 10, 5, 2)
# system.add_process(3, 8, 2, 1)
# system.add_process(6, 12, 1, 3)

#system.exec_algorithm(Fifo)
system.exec_algorithm(SJF)
#system.exec_algorithm(EDF)
print(system.get_next_execution_interval())
print(system.get_next_execution_interval())
print(system.get_next_execution_interval())
print(system.get_next_execution_interval())
print(system.current_time)
