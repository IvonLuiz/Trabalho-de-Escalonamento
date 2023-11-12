import matplotlib.pyplot as plt
from IPython.display import clear_output, display

class GanttChart:
    def __init__(self, overload_factor=1):
        self.num_processes = 0
        self.default_process_color = 'blue'
        self.overload_color = 'red'
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel('Tempo')
        self.ax.set_ylabel('Processos e Sobrecarga')
        self.time_points = []
        self.total_time = 0
        self.overload_factor = overload_factor
        self.process_intervals = []
        self.overload_intervals = []

    def add_process(self, process_id, execution_interval):
        self.num_processes += 1
        self.process_intervals.append((process_id, execution_interval))

    def update_chart(self, current_time):
        self.ax.clear()
        self.ax.set_xlabel('Tempo')
        self.ax.set_ylabel('Processos e Sobrecarga')
        y_labels = [f'P{i}' for i in range(1, self.num_processes + 1)]
        self.ax.set_yticks([i * 10 + 5 for i in range(self.num_processes)])
        self.ax.set_yticklabels(y_labels)
        self.ax.grid(True)

        for i, (pid, intervals) in enumerate(self.process_intervals):
            for start, end in intervals:
                if current_time >= start and current_time <= end:
                    time_width = min(current_time, end) - start
                    self.ax.broken_barh([(start, time_width)], (5 + i * 10, 9), facecolors=self.default_process_color)

        for process_id, overload_intervals in enumerate(self.overload_intervals):
            for start, end in overload_intervals:
                if current_time >= start and current_time <= end:
                    time_width = min(current_time, end) - start
                    self.ax.broken_barh([(start, time_width)], (5 + process_id * 10, 9), facecolors=self.overload_color)

        self.time_points.append(current_time)
        self.ax.set_xlim(0, self.total_time)
        self.ax.set_ylim(0, (self.num_processes + 1) * 10)
        self.ax.set_yticks([i * 10 + 5 for i in range(self.num_processes)])
        self.ax.set_yticklabels(y_labels)

    def animate(self):
        try:
            for current_time in range(self.total_time):
                self.update_chart(current_time)
                plt.pause(1)  # Adicione um atraso de 1 segundo
                clear_output(wait=True)

            # Adicione esta linha para exibir o estado final
            self.update_chart(self.total_time)

            # Use display() para exibir o gráfico final
            display(self.fig)

        except KeyboardInterrupt:
            pass

# Exemplo de uso
antt_chart = GanttChart()
antt_chart.add_process(1, [(0, 7)])  # Corrigido para aceitar uma lista de intervalos
antt_chart.total_time = 15
antt_chart.animate()
