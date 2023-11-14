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
    system.exec_algorithm(RoundRobin, 'fifo')

    print(system.execution_intervals)
    print(system.deadline_overrun_intervals)

    print("Estado inicial RAM/DISK")
    print(system.memory.ram.storage)
    print(system.memory.disk.storage)

    system.process_execution()

    print("Estado final RAM/DISK")
    print(system.memory.ram.storage)
    print(system.memory.disk.storage)


    # print("P1 entra na RAM")
    # print(system.memory.ram.storage)
    # print(system.memory.disk.storage)
    #
    # system.process_execution()
    #
    # print("P3 entra na RAM")
    # print(system.memory.ram.storage)
    # print(system.memory.disk.storage)
    #
    # system.process_execution()
    #
    # print("P2 entra na RAM")
    # print(system.memory.ram.storage)
    # print(system.memory.disk.storage)
