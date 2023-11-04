from algorithms.algorithm import Algorithm
from queue import Queue

class RoundRobin(Algorithm):

    def __init__(self, processes=[], overhead=1, quantum=2):
        self.processes = processes
        self.overhead = overhead
        self.quantum = quantum
    
    def execute(self):
        queue= Queue()
        time = 0
        
        for process in self.processes:
            queue.put(process)
            
        while not queue.empty():
            current_process = queue.get()
            
            if current_process.execution_time <= self.quantum:
                    # The process is completed within the current quantum
                    time += current_process.execution_time
                    current_process.execution_time = 0
                    print(f"Process {current_process.id} executed. Finish time: {time}")
            else:
                # O processo ainda tem tempo restante após o quantum
                time += self.quantum + self.overhead
                current_process.reduce_exec_time(self.quantum)
                print(f"Process {current_process.id} executed for {self.quantum} units. "
                f"Time to finish: {current_process.execution_time}. "
                f"Time: {time}")

                queue.put(current_process)