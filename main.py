from system import System
from algorithms.fifo import Fifo
from algorithms.sjf import SJF
from algorithms.round_robin import RoundRobin
from algorithms.edf import EDF

system = System(overhead=0, quantum=2)

system.add_process(0, 10, 5, 2)
system.add_process(3, 8, 2, 1)
system.add_process(6, 12, 1, 3)

system.exec_algorithm(Fifo)
system.exec_algorithm(SJF)
system.exec_algorithm(EDF)