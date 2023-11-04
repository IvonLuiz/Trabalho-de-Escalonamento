import matplotlib.pyplot as plt

class GanttChart:
    def __init__(self, process_intervals, overload_intervals=None):
        self.process_intervals = process_intervals
        self.overload_intervals = overload_intervals or []
        self.num_processes = len(process_intervals)
        self.default_process_color = 'blue'
        self.overload_color = 'red'

    def generate_chart(self):
        fig, gnt = plt.subplots()

        gnt.set_ylim(0, (self.num_processes + 1) * 10)

        max_time = max(
            end for intervals in self.process_intervals + self.overload_intervals
            for _, end in intervals
        )

        gnt.set_xlim(0, max_time + 1)

        gnt.set_xlabel('Tempo')
        gnt.set_ylabel('Processos e Sobrecarga')

        y_labels = [f'P{i}' for i in range(1, self.num_processes + 1)]

        gnt.set_yticks([i * 10 + 5 for i in range(self.num_processes)])
        gnt.set_yticklabels(y_labels)

        gnt.grid(True)

        for i, intervals in enumerate(self.process_intervals):
            for start, end in intervals:
                gnt.broken_barh([(start, end - start)], (5 + i * 10, 9), facecolors=self.default_process_color)

        for process, overload_intervals in zip(range(1, self.num_processes + 1), self.overload_intervals):
            for start, end in overload_intervals:
                gnt.broken_barh([(start, end - start)], (5 + (process - 1) * 10, 9), facecolors=self.overload_color)

        plt.show()

if __name__ == '__main__':
    process_intervals = [
        [(0, 2), (5, 7), (9, 12)],  # Processo 1
        [(3, 4), (8, 9)],  # Processo 2
        # Adicione intervalos para outros processos conforme necessário
    ]

    overload_intervals = [
        [(2, 3), (7, 8)],  # Sobrecarga para o Processo 1 (será representado em vermelho)
        [(4, 5)],  # Sobrecarga para o Processo 2 (será representado em vermelho)
        # Adicione intervalos de sobrecarga para outros processos conforme necessário
    ]

    gantt_chart = GanttChart(process_intervals, overload_intervals)
    gantt_chart.generate_chart()
