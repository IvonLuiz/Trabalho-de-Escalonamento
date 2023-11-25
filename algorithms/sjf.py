from algorithms.algorithm import Algorithm
from process import Process


class SJF(Algorithm):

    def __init__(self, processes=None, overhead=0, quantum=0):
        super().__init__(processes=processes)


    def execute(self):
        time = 0
        execution_intervals = {}
        deadline_overrun_intervals = {}
        
        while self.processes:
            eligible_processes = [p for p in self.processes if p.arrival_time <= time]

            if not eligible_processes:
                time += 1
                continue

            shortest_job = min(eligible_processes, key=lambda x: x.execution_time)

            start_time = time
            end_time = time + shortest_job.execution_time

            intervals = execution_intervals.get(shortest_job.id, [])
            intervals.append((start_time, end_time))
            execution_intervals[shortest_job.id] = intervals
            deadline_overrun_intervals[shortest_job.id] = self.__detect_deadline_overrun(shortest_job, time)

            time = end_time
            self.processes.remove(shortest_job)

        return execution_intervals, deadline_overrun_intervals


    def __detect_deadline_overrun(self, process: Process, time):
        return 0