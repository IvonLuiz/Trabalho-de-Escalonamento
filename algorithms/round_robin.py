from queue import Queue
from algorithms.algorithm import Algorithm
from process import Process


class RoundRobin(Algorithm):

    def __init__(self, processes=None, overhead=1, quantum=2):
        super().__init__(processes=processes, overhead=overhead, quantum=quantum)
        self.process_queue = Queue()

    def execute(self):
        time = 0
        current_process = None
        self.processes.sort(key=lambda x: x.arrival_time)
        execution_intervals = {}
        deadline_overrun_intervals = {}

        # Case process enters late
        time = self.__verify_late_arrival(time)
        
        while True:
            current_process = self.process_queue.get()
            
            if current_process.execution_time <= self.quantum:
                # The process is completed within the current quantum
                execution_intervals.setdefault(current_process.id, []).append((time, time + current_process.execution_time))
                time += current_process.execution_time
                deadline_overrun_intervals.setdefault(current_process.id, []).append(self.__detect_deadline_overrun(current_process, time))
                current_process.execution_time = 0
                
                self.__verify_arrival_while_processing(time)
            else:
                # The process still has time remaining after the quantum
                execution_intervals.setdefault(current_process.id, []).append((time, time + self.quantum))
                time += self.quantum + self.overhead
                current_process.reduce_exec_time(self.quantum)

                self.__verify_arrival_while_processing(time)
                self.process_queue.put(current_process)

            # Case process enters late
            time = self.__verify_late_arrival(time)
            
            if self.process_queue.empty():
                break

        return execution_intervals, deadline_overrun_intervals

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

    def __detect_deadline_overrun(self, process: Process, time):
        true_deadline = (process.arrival_time + process.deadline)

        # Returns 0 if there isen't deadline_overrun     
        if time > true_deadline:
            return true_deadline
        return 0
