import copy
import time
from process import Process
from algorithms.algorithm import Algorithm
from mmu import MemoryManagementUnit

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
    
    def __init__(self): #processes, overhead, quantum, delay
        self.processes = None
        self.overhead = 0
        self.quantum = 0
        self.current_time = 0
        self.execution_intervals = {}
        self.deadline_overrun_intervals = {}
        self.memory = None
        self.delay = 0

    def exec_algorithm(self, algorithm, paging_algorithm):
        process_copy = copy.copy(self.processes)
        process_copy_mmu = copy.copy(self.processes)
        algorithm_scheduler = self.get_algorithm_instance(algorithm)(process_copy)
        self.memory = MemoryManagementUnit(algorithm=paging_algorithm, processList=process_copy_mmu)
        self.execution_intervals, self.deadline_overrun_intervals = algorithm_scheduler.execute()

    def get_next_execution_interval(self):
        """
        Get the next execution interval for a process, update the current time, and return information.

        Returns:
        - result (tuple): Tuple containing (process_id, interval, has_overload).
        """
        closest_interval = None
        process_id = 0
        has_overload = False

        for it_process_id, intervals in self.execution_intervals.items():
            for start_time, end_time in intervals:
                if start_time >= self.current_time and (closest_interval is None or start_time < closest_interval[0]):
                    closest_interval = (start_time, end_time)
                    has_overload = (
                            intervals.index(closest_interval) + 1 < len(intervals)
                            and intervals[intervals.index(closest_interval) + 1][0] == closest_interval[1]
                    )
                    process_id = it_process_id

        if closest_interval is None:
            return None

        # Update the current time
        self.current_time = closest_interval[1] + (1 if has_overload else 0)

        return process_id, closest_interval, has_overload

    def get_process(self, process_id) -> Process:
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

            print(f"Processo id: {process_id} sendo executado.")

            # Carregar processo na memória
            self.load_process(current_process)
            print(self.memory.disk.storage)
            print(self.memory.ram.storage)
            # # Atualizar gráfico Gantt
            # self.update_gantt_chart(process_id, interval, has_overload)
            #
            # # Atualizar gráfico de memória
            # self.update_memory_plot()
            #
            # # Verificar deadline_overrun e atualizar o gráfico de Gantt
            # self.check_and_update_deadline_overrun(process_id, interval)
            time.sleep(self.delay)
            

    def load_process(self, process: Process):
        """
        Load process into memory.

        Parameters:
        - process (Process): Process object to load into memory.
        """

        id = process.id
        number_of_pages = process.number_of_pages

        self.memory.load(id, number_of_pages)

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

    def calculate_average_turnaround(self):
        total_turnaround = 0
        number_of_processes = len(self.execution_intervals)

        for process_id, intervals in self.execution_intervals.items():
            arrival_time = self.get_process(process_id).arrival_time
            total_execution_time = 0

            if intervals:
                last_interval = intervals[-1]
                total_execution_time = last_interval[1]

            turnaround = total_execution_time - arrival_time
            total_turnaround += turnaround

        average_turnaround = total_turnaround / number_of_processes
        return average_turnaround

    #Set
    def set_processes_list(self, processes):
        self.processes = processes

    def set_quantum(self, quantum):
        self.quantum = quantum

    def set_overhead(self, overhead):
        self.overhead = overhead

    def set_delay(self, delay):
        self.delay = delay

    def get_algorithm_instance(self, algorithm_name):
        algorithm_name_lower = algorithm_name.lower()

        # "Switch case" simples para diferentes algoritmos
        if algorithm_name_lower == 'fifo':
            from algorithms.fifo import Fifo
            return Fifo
        elif algorithm_name_lower == 'sjf':
            from algorithms.sjf import SJF
            return SJF
        elif algorithm_name_lower == 'edf':
            from algorithms.edf import EDF
            return EDF
        elif algorithm_name_lower == 'rr':
            from algorithms.round_robin import RoundRobin
            return RoundRobin
        else:
            print(f"Algoritmo desconhecido: {algorithm_name}")
            return None