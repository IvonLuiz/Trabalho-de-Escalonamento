from system import System
from algorithms.fifo import Fifo
from algorithms.sjf import SJF
from algorithms.edf import EDF
from algorithms.round_robin import RoundRobin
from csv_reader import CSVReader
from process import Process

CSV_FILE = "csv/input_file.csv"

# Example usage
if __name__ == "__main__":
    processes = CSVReader(CSV_FILE).get_processes()
    system = System(processes, overhead=1, quantum=2)

    system.exec_algorithm(RoundRobin)

    print(system.processes)
    print(system.execution_intervals)
    print(system.deadline_overrun_intervals)
    print(system.calculate_average_turnaround())
