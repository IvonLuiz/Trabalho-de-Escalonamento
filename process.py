class Process:

    def __init__(self, id, exec_time, priority, deadline, number_of_pages=5, arrival_time=0) -> None:
        self.id = id
        self.arrival_time = arrival_time
        self.execution_time = exec_time
        self.deadline = deadline
        self.priority = priority
        self.number_of_pages = number_of_pages

    def reduce_exec_time(self, time_reduce):
        self.execution_time -= time_reduce

