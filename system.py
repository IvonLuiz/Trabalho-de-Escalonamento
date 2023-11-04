from process import Process
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
        algorithm_scheduler = algorithm(self.processes, self.overhead)
        algorithm_scheduler.execute()
