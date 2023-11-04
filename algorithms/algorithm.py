class Algorithm:
    """This class follows command pattern"""
    def __init__(self, processes=[]):
        """Interface for scheduling algorithms"""
        self.processes = processes

    def execute(self) -> None:
        """Abstract method"""
        raise NotImplementedError("No execution implemented")