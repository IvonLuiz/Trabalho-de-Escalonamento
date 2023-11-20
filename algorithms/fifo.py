from algorithms.algorithm import Algorithm
from process import Process


class Fifo(Algorithm):

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


# Example usage
if __name__ == "__main__":
    processes = [
        Process(id=1, exec_time=5, priority=1, deadline=10, arrival_time=0),
        Process(id=2, exec_time=3, priority=2, deadline=8, arrival_time=1),
        Process(id=3, exec_time=7, priority=3, deadline=15, arrival_time=2),
    ]

    fifo_scheduler = Fifo(processes)
    execution_intervals, deadline_overrun_intervals = fifo_scheduler.execute()

    print(execution_intervals)
    print(deadline_overrun_intervals)
    
    print("Execution Intervals:")
    for process_id, interval in execution_intervals.items():
        print(f"Process {process_id}: {interval}")
