from algorithms.algorithm import Algorithm
from process import Process


class Fifo(Algorithm):

    def execute(self):
        self.processes.sort(key=lambda x: x.arrival_time)  # Orders processes based on arrival time
        current_time = 0
        execution_intervals = {}  # Dictionary to store execution intervals for each process

        for process in self.processes:
            # Check if the new process in the queue arrived in less time than the current one
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            intervals = []
            start_time = current_time

            while process.execution_time > 0:
                current_time += 1
                process.reduce_exec_time(1)

            end_time = current_time

            intervals.append((start_time, end_time))

            execution_intervals[process.id] = intervals

            print(f"Process {process.id} executed. Intervals: {intervals}")

        return execution_intervals


# Example usage
if __name__ == "__main__":
    processes = [
        Process(id=1, exec_time=5, priority=1, deadline=10, arrival_time=0),
        Process(id=2, exec_time=3, priority=2, deadline=8, arrival_time=1),
        Process(id=3, exec_time=7, priority=3, deadline=15, arrival_time=2),
    ]

    fifo_scheduler = Fifo(processes)
    execution_intervals = fifo_scheduler.execute()

    print(execution_intervals)

    print("Execution Intervals:")
    for process_id, interval in execution_intervals.items():
        print(f"Process {process_id}: {interval}")
