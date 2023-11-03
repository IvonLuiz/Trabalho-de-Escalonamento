from system import System
from fifo import Fifo


sistema = System(0)

# Adicione os processos conforme necessário
sistema.add_process(0, 10, 1, 2)
sistema.add_process(3, 8, 2, 1)

sistema.add_process(6, 12, 3, 3)

# Execute o escalonamento FIFO
fifo_scheduler = Fifo(sistema.processes)
fifo_scheduler.execute()