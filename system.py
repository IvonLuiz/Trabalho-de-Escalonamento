from process import Process
from algorithms.algorithm import Algorithm

class System:
    """
    A class representing a system for managing processes. The system schedules processes using a specified algorithm.
    
    Attributes:
    - overhead (int): The overhead time for the system.
    - quantum (int): The time quantum for the scheduling algorithm.
    - processes (list): A list of processes in the system.
    
    Methods:
    - exec_algorithm(algorithm): Execute a scheduling algorithm on the processes.
    """
    
    def __init__(self, processes, overhead, quantum):
        self.processes = processes
        self.overhead = overhead
        self.quantum = quantum
        self.current_time = 0
        self.execution_intervals = {}
        self.deadline_overrun_intervals = {}

    def exec_algorithm(self, algorithm: Algorithm):
        algorithm_scheduler = algorithm(self.processes)
        self.execution_intervals, self.deadline_overrun_intervals = algorithm_scheduler.execute()

    def get_next_execution_interval(self):
        """
        Get the next execution interval for a process, update the current time, and return information.

        Returns:
        - result (tuple): Tuple containing (process_id, interval, has_overload).
        """
        
        for process_id, intervals in self.execution_intervals.items():
            closest_interval = None

            for start_time, end_time in intervals:
                if start_time >= self.current_time and (closest_interval is None or start_time < closest_interval[0]):
                    closest_interval = (start_time, end_time)

            if closest_interval:
                has_overload = (
                    intervals.index(closest_interval) + 1 < len(intervals)
                    and intervals[intervals.index(closest_interval) + 1][0] == closest_interval[1]
                )

                # Update the current time
                self.current_time = closest_interval[1] + (1 if has_overload else 0)

                return process_id, closest_interval, has_overload

        return None

    def get_process(self, process_id):
        """
        Get the process object by ID.

        Parameters:
        - process_id (int): ID of the process.

        Returns:
        - process (Process): Process object.
        """
        for process in self.processes:
            if process.id == process_id:
                return process
        return None

    def process_execution(self):
        """
        Process execution loop.
        """
        while True:
            result = self.get_next_execution_interval()
            if result is None:
                break
            process_id, interval, has_overload = result
            current_process = self.get_process(process_id)

            # Atualizar gráfico Gantt
            self.update_gantt_chart(process_id, interval, has_overload)

            # Carregar processo na memória
            self.load_process(current_process)

            # Atualizar gráfico de memória
            self.update_memory_plot()
            
            # Verificar deadline_overrun e atualizar o gráfico de Gantt
            self.check_and_update_deadline_overrun(process_id, interval)

    def load_process(self, process):
        """
        Load process into memory.

        Parameters:
        - process (Process): Process object to load into memory.
        """
        # Implemente a lógica de carregamento do processo na memória aqui
        pass

    def update_gantt_chart(self, process_id, interval, has_overload):
        """
        Update Gantt chart with the latest execution interval.

        Parameters:
        - process_id (int): ID of the executed process.
        - interval (tuple): Execution interval.
        - has_overload (bool): Indicates if there is overload after the interval.
        """
        # Implemente a lógica de atualização do gráfico Gantt aqui
        pass

    def update_memory_plot(self):
        """
        Update memory plot.
        """
        # Implemente a lógica de atualização do gráfico de memória aqui
        pass
    
##-----AINDA É PRECISO TESTAR ESSA PARTE-----#
    def check_and_update_deadline_overrun(self, process_id, interval):
            """
            Check for deadline_overrun and update the Gantt chart accordingly.

            Parameters:
            - process_id (int): ID of the executed process.
            - interval (tuple): Execution interval.
            """
            process = self.get_process(process_id)
            true_deadline = process.arrival_time + process.deadline

            # Verificar se houve deadline_overrun no intervalo
            if interval[1] > true_deadline:
                overload_start = max(interval[0], true_deadline)
                overload_interval = (overload_start, interval[1])

                # Atualizar o gráfico de Gantt com a sobrecarga
                self.update_gantt_chart(process_id, overload_interval, True)