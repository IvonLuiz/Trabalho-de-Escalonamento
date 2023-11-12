from algorithms.algorithm import Algorithm
from process import Process


class SJF(Algorithm):

    def execute(self):
        current_time = 0
        execution_intervals = {}  # Dictionary to store execution intervals for each process

        while self.processes:
            eligible_processes = [p for p in self.processes if p.arrival_time <= current_time]

            if not eligible_processes:
                current_time += 1
                continue

            shortest_job = min(eligible_processes, key=lambda x: x.execution_time)

            start_time = current_time
            end_time = current_time + shortest_job.execution_time

            intervals = execution_intervals.get(shortest_job.id, [])
            intervals.append((start_time, end_time))
            execution_intervals[shortest_job.id] = intervals

            current_time = end_time
            self.processes.remove(shortest_job)

            print(f"Process {shortest_job.id} executed. Intervals: {intervals}")

        return execution_intervals



if __name__ == "__main__":
    processes = [
        Process(id=1, exec_time=5, priority=1, deadline=10, arrival_time=0),
        Process(id=2, exec_time=7, priority=2, deadline=8, arrival_time=1),
        Process(id=3, exec_time=3, priority=3, deadline=15, arrival_time=2),
    ]

    sjf_scheduler = SJF(processes)
    execution_intervals = sjf_scheduler.execute()

    print("Execution Intervals:")
    for process_id, interval in execution_intervals.items():
        print(f"Process {process_id}: {interval}")