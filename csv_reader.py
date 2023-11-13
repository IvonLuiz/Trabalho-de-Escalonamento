import csv
from process import Process


class CSVReader:

    def __init__(self, csv_file: str):
        self.csv_file = csv_file

    def get_processes(self):
        processes = []

        with open(self.csv_file, 'r') as f:
            reader = csv.reader(f)
            first, *rest = reader
            for row in rest:
                process = self.create_process(first, row)
                processes.append(process)

        return processes

    def create_process(self, props, values):
        # Extract the values from the CSV row
        id, arrival_time, execution_time, deadline, priority, number_of_pages = map(int, values)

        # Create a Process instance with the extracted values
        process = Process(id, execution_time, priority, deadline, number_of_pages, arrival_time)

        return process


if __name__ == '__main__':
    csv_file = 'csv/input_file.csv'
    for process in CSVReader(csv_file).get_processes():
        print(f"Process ID: {process.id}")
        print(f"Arrival Time: {process.arrival_time}")
        print(f"Execution Time: {process.execution_time}")
        print(f"Deadline: {process.deadline}")
        print(f"Priority: {process.priority}")
        print(f"Number of Pages: {process.number_of_pages}")
        print()