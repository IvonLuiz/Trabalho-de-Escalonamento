import matplotlib.pyplot as plt
from IPython.display import clear_output
import time
import pandas as pd

class MemorySimulation:
    def __init__(self, memory_size, page_size, process_durations, pages_per_process):
        self.memory_size = memory_size
        self.page_size = page_size
        self.pages = int(memory_size / page_size)
        self.process_durations = process_durations
        self.pages_per_process = pages_per_process
        self.memory = pd.DataFrame(data=[['' for _ in range(10)] for _ in range(5)])
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Colunas (Páginas)')
        self.ax.set_ylabel('Linhas (Processos)')
        self.total_time = sum(process_durations)
        self.current_time = 0

    def allocate_memory(self, process_index):
        process_name = f'P{process_index + 1}'
        start_page = process_index * self.pages_per_process
        end_page = start_page + self.pages_per_process

        # Alocar todas as páginas de uma vez
        for i in range(start_page, end_page):
            row, col = divmod(i, 10)
            self.memory.iloc[row, col] = process_name

        self.display_memory()

    def display_memory(self):
        self.ax.clear()
        self.ax.matshow([[1 if cell else 0 for cell in row] for row in self.memory.values], cmap='gray', aspect='auto')
        self.ax.set_xlabel('Colunas (Páginas)')
        self.ax.set_ylabel('Linhas (Processos)')
        self.ax.set_xticks(range(10))
        self.ax.set_yticks(range(5))
        for i in range(5):
            for j in range(10):
                text = self.memory.iloc[i, j]
                self.ax.text(j, i, text, ha='center', va='center', color='black' if text else 'white')
                self.ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False, color='black', linestyle='dashed'))
        self.ax.grid(False)
        self.fig.canvas.draw()
        plt.pause(0.1)
        clear_output(wait=True)

    def simulate_memory_allocation(self):
        try:
            for process_index, duration in enumerate(self.process_durations):
                self.allocate_memory(process_index)
                self.current_time += duration
                time.sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    process_durations = [2, 2, 2, 1]  # Durações dos processos
    memory_simulation = MemorySimulation(memory_size=200, page_size=4, process_durations=process_durations, pages_per_process=7)
    memory_simulation.simulate_memory_allocation()
