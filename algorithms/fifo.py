from algorithms.algorithm import Algorithm
from process import Process


class Fifo(Algorithm):
    
    def __init__(self, processes=None, overhead=0, quantum=0):
        super().__init__(processes=processes)
    
    
    def execute(self):
        self.processes.sort(key=lambda x: x.arrival_time)  # Orders processes based on arrival time
        time = 0
        execution_intervals = {}
        deadline_overrun_intervals = {}
        
        for process in self.processes:
            # Check if the new process in the queue arrived in less time than the current one
            if time < process.arrival_time:
                time = process.arrival_time

            intervals = []
            start_time = time

            while process.execution_time > 0:
                time += 1
                process.reduce_exec_time(1)

            intervals.append((start_time, time))

            execution_intervals[process.id] = intervals
            deadline_overrun_intervals[process.id] = self.__detect_deadline_overrun(process, time)

        return execution_intervals, deadline_overrun_intervals


    def __detect_deadline_overrun(self, process: Process, time):
        return 0