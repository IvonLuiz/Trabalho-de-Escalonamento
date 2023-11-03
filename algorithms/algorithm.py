class Algorithm:

    def __init__(self, processes=[]):
        """Interface for scheduling algorithms"""
        self.processes = processes

    def execute(self):
        pass