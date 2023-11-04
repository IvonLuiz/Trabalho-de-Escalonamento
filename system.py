from process import Process
from algorithms.fifo import Fifo
from algorithms.sjf import SJF
from algorithms.round_robin import RoundRobin
from algorithms.edf import EDF
from algorithms.algorithm import Algorithm

class System:
    def __init__(self, overhead, quantum):
        self.processes = []
        self.overhead = overhead
        self.quantum = quantum
        
    def add_process(self, arrival_time, exec_time, deadline, priority):
        process_id = len(self.processes) + 1
        process = Process(id            = process_id, 
                          exec_time     = exec_time, 
                          priority      = priority, 
                          deadline      = deadline, 
                          arrival_time  = arrival_time)

        process.system_overhead = self.overhead
        self.processes.append(process)
        
    def exec_algorithm(self, algorithm: Algorithm):
        algorithm_scheduler = algorithm(self.processes)
        algorithm_scheduler.execute()
