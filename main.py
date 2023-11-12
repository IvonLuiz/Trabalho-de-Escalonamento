from system import System
from algorithms.fifo import Fifo
from algorithms.sjf import SJF
from algorithms.round_robin import RoundRobin
from algorithms.edf import EDF

system = System(overhead=1, quantum=2)

# system.add_process(arrival_time=0, exec_time=4, deadline=7, priority=2)
# system.add_process(arrival_time=2, exec_time=2, deadline=5, priority=2)
# system.add_process(arrival_time=4, exec_time=1, deadline=8, priority=2)
# system.add_process(arrival_time=6, exec_time=3, deadline=10, priority=2)

system.add_process(arrival_time=0, exec_time=5, deadline=7, priority=2)
system.add_process(arrival_time=3, exec_time=3, deadline=5, priority=2)
system.add_process(arrival_time=7, exec_time=10, deadline=8, priority=2)
system.add_process(arrival_time=8, exec_time=2, deadline=10, priority=2)
system.add_process(arrival_time=10, exec_time=4, deadline=10, priority=2)

# system.add_process(arrival_time=0, exec_time=5, deadline=7, priority=2)
# system.add_process(arrival_time=1, exec_time=2, deadline=5, priority=2)
# system.add_process(arrival_time=12, exec_time=7, deadline=8, priority=2)

# system.exec_algorithm(Fifo)
# system.exec_algorithm(SJF)
# system.exec_algorithm(RoundRobin)
system.exec_algorithm(EDF)