from algorithms.algorithm import Algorithm
from process import Process


class EDF(Algorithm):

    def __init__(self, processes=[], overhead=1, quantum=2):
        self.processes = processes
        self.overhead = overhead
        self.quantum = quantum
        self.process_queue = {} # Keys: process, Values: deadline - execution_time

    def execute(self):
        time = 0
        current_process = None
        # Case process enters late
        self.__verify_late_arrival(time)

        while True:
            current_process = next(iter(self.process_queue), None)
            del self.process_queue[current_process]

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
                self.__add_process_with_priority(current_process, time)

            # Case process enters late
            time = self.__verify_late_arrival(time)

            if len(self.process_queue) == 0:
                break


    def __verify_arrival_while_processing(self, time):
        to_remove = []
        for i, proc in enumerate(self.processes):
            if proc.arrival_time <= time:
                self.__add_process_with_priority(proc, time)
                to_remove.append(i)

        for index in reversed(to_remove):
            self.processes.pop(index)


    def __verify_late_arrival(self, time):
        if len(self.process_queue) == 0 and len(self.processes) > 0:
            proc = self.processes[0]
            self.__add_process_with_priority(proc, time)
            self.processes.pop(0)
            time = proc.arrival_time
        return time


    def __add_process_with_priority(self, process, time):
        # Calculate the priority (value) for the process and add it to the process_queue dictionary
        self.process_queue[process] = process.deadline - time

        # Sort the dictionary based on values
        sorted_queue = sorted(self.process_queue.items(), key=lambda item: item[1])

        # Create a new sorted dictionary
        sorted_dict = {key: value for key, value in sorted_queue}

        # Update the original dictionary (self.process_queue) with the new sorted dictionary
        self.process_queue = sorted_dict


if __name__ == "__main__":
    processes = [
        Process(id=1, exec_time=5, priority=1, deadline=10, arrival_time=0),
        Process(id=2, exec_time=3, priority=2, deadline=8, arrival_time=1),
        Process(id=3, exec_time=7, priority=3, deadline=15, arrival_time=2),
    ]

    edf = EDF(processes)
    execution_intervals = edf.execute()

    print(execution_intervals)

    print("Execution Intervals:")
    for process_id, interval in execution_intervals.items():
        print(f"Process {process_id}: {interval}")