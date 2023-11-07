import matplotlib.pyplot as plt
from IPython.display import clear_output
import time

class GanttChart:
    def __init__(self, process_intervals, overload_intervals=None):
        self.process_intervals = process_intervals
        self.overload_intervals = overload_intervals or []
        self.num_processes = len(process_intervals)
        self.default_process_color = 'blue'
        self.overload_color = 'red'
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Tempo')
        self.ax.set_ylabel('Processos e Sobrecarga')
        self.time_points = []
        self.total_time = max(
            end for intervals in self.process_intervals + self.overload_intervals
            for _, end in intervals
        ) + 1

    def generate_chart(self, current_time):
        self.ax.clear()
        self.ax.set_xlabel('Tempo')
        self.ax.set_ylabel('Processos e Sobrecarga')
        y_labels = [f'P{i}' for i in range(1, self.num_processes + 1)]
        self.ax.set_yticks([i * 10 + 5 for i in range(self.num_processes)])
        self.ax.set_yticklabels(y_labels)
        self.ax.grid(True)

        for i, intervals in enumerate(self.process_intervals):
            for start, end in intervals:
                if current_time >= start:
                    time_width = min(current_time, end) - start
                    self.ax.broken_barh([(start, time_width)], (5 + i * 10, 9), facecolors=self.default_process_color)

        for process, overload_intervals in enumerate(self.overload_intervals):
            for start, end in overload_intervals:
                if current_time >= start:
                    time_width = min(current_time, end) - start
                    self.ax.broken_barh([(start, time_width)], (5 + process * 10, 9), facecolors=self.overload_color)

        self.time_points.append(current_time)
        self.ax.set_xlim(0, self.total_time)
        self.ax.set_ylim(0, (self.num_processes + 1) * 10)
        self.ax.set_yticks([i * 10 + 5 for i in range(self.num_processes)])
        self.ax.set_yticklabels(y_labels)

    def animate(self):
        try:
            for current_time in range(self.total_time):
                self.generate_chart(current_time)
                plt.pause(1)  # Adicione um atraso de 1 segundo
                clear_output(wait=True)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    process_intervals = [
        [(0, 2), (5, 7), (13, 14)],  # Processo 1
        [(3, 4), (8, 9)],  # Processo 2
        [(9, 12), (14, 19)],  # Processo 3
        # Adicione intervalos para outros processos conforme necessário
    ]

    overload_intervals = [
        [(2, 3), (7, 8)],  # Sobrecarga para o Processo 1 (será representado em vermelho)
        [(4, 5)],  # Sobrecarga para o Processo 2 (será representado em vermelho)
        [(12, 13)],  # Sobrecarga para o Processo 3 (será representado em vermelho)
        # Adicione intervalos de sobrecarga para outros processos conforme necessário
    ]

    gantt_chart = GanttChart(process_intervals, overload_intervals)
    gantt_chart.animate()
