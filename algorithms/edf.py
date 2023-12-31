from algorithms.algorithm import Algorithm
from process import Process


class EDF(Algorithm):

    def __init__(self, processes=[], overhead=1, quantum=2):
        super().__init__(processes=processes, overhead=overhead, quantum=quantum)
        self.process_queue = {} # Keys: process, Values: deadline - execution_time

    def execute(self):
        time = 0
        current_process = None
        self.processes.sort(key=lambda x: x.arrival_time)
        execution_intervals = {}
        deadline_overrun_intervals = {}

        # Case process enters late
        time = self.__verify_late_arrival(time)
            
        while True:
            current_process = next(iter(self.process_queue), None)
            del self.process_queue[current_process]

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

                
                added = self.__add_process_with_priority(current_process, time)
                if (added == False):
                    self.__verify_arrival_while_processing(time)

            # Case process enters late
            time = self.__verify_late_arrival(time)

            if len(self.process_queue) == 0:
                break
        
        return execution_intervals, deadline_overrun_intervals


    def __verify_arrival_while_processing(self, time):
        to_remove = []
        added = False
        for i, proc in enumerate(self.processes):
            if proc.arrival_time <= time:
                self.__add_process_with_priority(proc, time)
                to_remove.append(i)
                added = True
                
        for index in reversed(to_remove):
            self.processes.pop(index)
            
        return added


    def __verify_late_arrival(self, time):
        if len(self.process_queue) == 0 and len(self.processes) > 0:
            proc = self.processes[0]
            self.__add_process_with_priority(proc, time)
            self.processes.pop(0)
            time = proc.arrival_time
        return time


    def __add_process_with_priority(self, process, time):
        # Calculate the priority (value) for the process and add it to the process_queue dictionary
        self.process_queue[process] = process.deadline + process.arrival_time 

        # Sort the dictionary based on values
        sorted_queue = sorted(self.process_queue.items(), key=lambda item: item[1])

        # Create a new sorted dictionary
        sorted_dict = {key: value for key, value in sorted_queue}

        # Update the original dictionary (self.process_queue) with the new sorted dictionary
        self.process_queue = sorted_dict
        

    def __detect_deadline_overrun(self, process: Process, time):
        true_deadline = (process.arrival_time + process.deadline)

        # Returns 0 if there isen't deadline_overrun     
        if time > true_deadline:
            return true_deadline
        return 0