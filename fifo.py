from process import Process
from algorithm import Algorithm

class Fifo(Algorithm):
    def __init__(self, processes=[]):
        self.processes = processes

    def execute(self):
        self.processes.sort(key=lambda x: x.arrival_time)  # Ordena os processos com base no tempo de chegada
        current_time = 0

        for process in self.processes:
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            current_time += process.execution_time
            print(f"Process {process.id} executed. Finish time: {current_time}")

