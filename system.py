from process import Process
from algorithms.algorithm import Algorithm

class System:
    """
    A class representing a system for managing processes. The system schedules processes using a specified algorithm.
    
    Attributes:
    - overhead (int): The overhead time for the system.
    - quantum (int): The time quantum for the scheduling algorithm.
    - processes (list): A list of processes in the system.
    
    Methods:
    - add_process(arrival_time, exec_time, deadline, priority=0): Add a new process to the system.
    - exec_algorithm(algorithm): Execute a scheduling algorithm on the processes.
    """
    
    def __init__(self, overhead, quantum):
        self.processes = []
        self.overhead = overhead
        self.quantum = quantum
        
    def add_process(self, arrival_time, exec_time, deadline, priority=0):
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
