from algorithms.algorithm import Algorithm

class SJF(Algorithm):

    def execute(self):
        self.processes.sort(key=lambda x: x.execution_time)  # Orders processes based on execution time
        current_time = 0

        for process in self.processes:
            # Check if the new process in the queue arrived in less time than the current one
            # if current_time < process.arrival_time:
            #     current_time = process.arrival_time

            current_time += process.execution_time
            print(f"Process {process.id} executed. Finish time: {current_time}")
