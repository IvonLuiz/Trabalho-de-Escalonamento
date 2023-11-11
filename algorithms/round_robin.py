from queue import Queue
from algorithms.algorithm import Algorithm

class RoundRobin(Algorithm):

    def __init__(self, processes=[], overhead=1, quantum=2):
        self.processes = processes
        self.overhead = overhead
        self.quantum = quantum
        self.process_queue = Queue()

    def execute(self):
        time = 0
        current_process = None
        # Case process enters late
        self.__verify_late_arrival(time)

        while True:
            current_process = self.process_queue.get()
                            
            if current_process.execution_time <= self.quantum:
                # The process is completed within the current quantum
                time += current_process.execution_time
                current_process.execution_time = 0
                print(f"Process {current_process.id} executed. Finish time: {time}")
                self.__verify_arrival_while_processing(time)
            else:
                # The process still has time remaining after the quantum
                time += self.quantum + self.overhead
                current_process.reduce_exec_time(self.quantum)
                print(f"Process {current_process.id} executed for {self.quantum} units. "
                f"Time to finish: {current_process.execution_time}. "
                f"Time: {time}")
                
                self.__verify_arrival_while_processing(time)
                self.process_queue.put(current_process)
        
            # Case process enters late
            time = self.__verify_late_arrival(time)
            
            if self.process_queue.empty():
                break


    def __verify_arrival_while_processing(self, time):
        to_remove = []
        for i, proc in enumerate(self.processes):
            if proc.arrival_time <= time:
                self.process_queue.put(proc)
                to_remove.append(i)  
                
        for index in reversed(to_remove):
            self.processes.pop(index)

    def __verify_late_arrival(self, time):
        if self.process_queue.empty() and len(self.processes) > 0:
            proc = self.processes[0]
            self.process_queue.put(proc)
            self.processes.pop(0)
            time = proc.arrival_time
        return time