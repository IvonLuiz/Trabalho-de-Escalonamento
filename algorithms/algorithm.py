class Algorithm:
    """This class follows command pattern"""
    
    def __init__(self, processes=None, overhead=0, quantum=0):
        """Interface for scheduling algorithms"""
        self.processes = processes or []
        self.overhead = overhead
        self.quantum = quantum

    def execute(self) -> None:
        """Abstract method"""
        raise NotImplementedError("No execution implemented")
    
    def __detect_deadline_overrun(self, process, time) -> None:
        raise NotImplementedError("No execution implemented")