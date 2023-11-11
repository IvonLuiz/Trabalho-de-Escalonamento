from memory.ramMemory import Ram
from memory.diskMemory import Disk
from process import Process


process= []
#id, exec_time, priority, deadline, number_of_pages=5, arrival_time=0
process.append(Process(1, 0, 10, 5, 20, 0))
process.append(Process(2, 3, 8, 2, 13, 0))
process.append(Process(3, 6, 12, 1, 15, 0))
process.append(Process(4, 0, 10, 5, 10, 0))
process.append(Process(9, 0, 10, 5, 43, 0))



class MemoryManagementUnit:
    def __init__(self, algorithm, processList) -> None:
        self.ram= Ram(50,50)
        self.disk= Disk(250, 250)
        self.processList= processList

        while len(processList)>0:
            self.disk.storeItem(self.processList[0].id, self.processList[0].number_of_pages)
            self.processList.pop(0)
        print(self.disk.storage)


mmu= MemoryManagementUnit('fifo', process)        

   #TODO def load(processId):