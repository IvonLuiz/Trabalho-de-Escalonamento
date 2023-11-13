from system import System
from algorithms.fifo import Fifo
from algorithms.sjf import SJF
from algorithms.edf import EDF
from algorithms.round_robin import RoundRobin
from csv_reader import CSVReader
from process import Process

# processes = [
#     Process(id=1, exec_time=5, priority=1, deadline=10, arrival_time=0),
#     Process(id=2, exec_time=3, priority=2, deadline=8, arrival_time=1),
#     Process(id=3, exec_time=7, priority=3, deadline=30, arrival_time=2),
# ]

# rr = RoundRobin(processes)
# execution_intervals, overload_intervals = rr.execute()

# print(execution_intervals)
# print(overload_intervals)

# print("Execution Intervals:")


# for process_id, interval in execution_intervals.items():
#     print(f"Process {process_id}: {interval}")
    

# if __name__ == "__main__":
#     processes = [
#         Process(id=1, exec_time=5, priority=1, deadline=10, arrival_time=0),
#         Process(id=2, exec_time=3, priority=2, deadline=8, arrival_time=1),
#         Process(id=3, exec_time=7, priority=3, deadline=10, arrival_time=2),
#     ]

#     edf = EDF(processes)
#     execution_intervals, overload_intervals = edf.execute()

#     print("Execution Intervals:")
#     for process_id, interval in execution_intervals.items():
#         print(f"Process {process_id}: {interval}")
#     print("Overload Intervals:")
#     for process_id, overloads in overload_intervals.items():
#         print(f"Process {process_id}: {overloads}")

# Example usage
if __name__ == "__main__":
    processes = [
        Process(id=1, exec_time=5, priority=1, deadline=10, arrival_time=0),
        Process(id=2, exec_time=3, priority=2, deadline=8, arrival_time=1),
        Process(id=3, exec_time=7, priority=3, deadline=15, arrival_time=2),
    ]

    fifo_scheduler = Fifo(processes)
    execution_intervals, overload_intervals = fifo_scheduler.execute()

    print(execution_intervals)
    print(overload_intervals)
    
    print("Execution Intervals:")
    for process_id, interval in execution_intervals.items():
        print(f"Process {process_id}: {interval}")
