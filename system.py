from process import Process

class System:
    def __init__(self):
        self.processes = []

    def add_process(self, arrival_time, execution_time, deadline, priority, system_overhead):
        process_id = len(self.processes) + 1
        process = Process(process_id, execution_time, priority, deadline, arrival_time)
        process.system_overhead = system_overhead
        self.processes.append(process)