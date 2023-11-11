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
        self.algorithm= algorithm
        self.removalQueue= [0] #A lista inicia sem nenhum processo (ID 0 = Espaço livre na RAM)
        self.pages= [50] #A ram inicia com 50 páginas alocadas ao ID 0 = Espaço livre na RAM

        #Construção inicial do disco
        while len(processList)>0:
            self.disk.storeItem(self.processList[0].id, self.processList[0].number_of_pages)
            self.processList.pop(0)



  

    def load(self, processId, numberOfPages):
        if self.algorithm == 'fifo':
            self.fifo(processId, numberOfPages)
        else:
            self.lru(processId, numberOfPages)


    def lookup(self, processId, numberOfPages):
        try:
            index= self.removalQueue.index(processId)
        except:
            index= -1

        if index != -1: #Processo está na memória
            if self.pages[index] == numberOfPages: #Processo está na memória em sua integridade (HIT)
                return self.pages[index]
        else: #Processo não está na memória
            return 0


    def ramWrite(self, processId, numberOfPages):
         #Busca em pages quanto de espaço é necessário para acomodar o processo na RAM
        lookup= self.lookup(processId, numberOfPages)
        spaceNeeded= numberOfPages-lookup
        pagesWritten= 0

        if processId == self.removalQueue[0] and spaceNeeded>0:
            self.removalQueue.pop(0)
            self.pages.pop(0)

        while spaceNeeded>0:
            if self.ram.storageLeft > 0:
                #Remover os dados do processo do disco
                if spaceNeeded < self.ram.storageLeft:
                    self.disk.removeItem(processId, spaceNeeded)
                else:
                    self.disk.removeItem(processId, self.ram.storageLeft)

            written= self.ram.write(processId, self.removalQueue[0], spaceNeeded)

            #Retirar do disco a quantidade que foi passada para a ram
            self.disk.removeItem(processId, written)

            #Colocar no disco a quantidade que eu sobreescrevi na ram
            self.disk.storeItem(self.removalQueue[0], written)

            spaceNeeded-= written
            pagesWritten+=written
            self.pages[0]-=written
            if self.pages[0] <= 0:
                self.removalQueue.pop(0)
                self.pages.pop(0)
            
            
        
        return pagesWritten



    def fifo(self, processId, numberOfPages):
        pagesWritten= self.ramWrite(processId, numberOfPages)
        if pagesWritten == 0: #Processo está na memória em sua integridade (HIT)
            return
        else:

            #Houve escrita na memória e um processo entrou na lista de remoção FIFO no final
            self.removalQueue.append(processId)
            self.pages.append(numberOfPages)
            return




    def lru(self, processId, numberOfPages):
        pagesWritten= self.ramWrite(processId, numberOfPages)
        if pagesWritten == 0: #Processo está na memória em sua integridade (HIT)
             
            #Encontro o local do processo na lista de remoção
            index= self.removalQueue.index(processId)
            self.removalQueue.pop(index) #Removo da lista de remoção no index encontrado
            self.pages.pop(index) #Removo da lista de páginas no index encontrado

            #Coloco o processo no fim da lista de remoção pois foi o processo mais recente
            self.removalQueue.append(processId)
            #Coloco o processo no fim da lista páginas pois foi o processo mais recente
            self.pages.append(numberOfPages)
            return
        else:

            #Houve escrita na memória e um processo entrou na lista de remoção FIFO no final
            self.removalQueue.append(processId)
            self.pages.append(numberOfPages)   
            return     

    



"""process= []
#id, exec_time, priority, deadline, number_of_pages=5, arrival_time=0
process.append(Process(1, 0, 10, 5, 20, 0))
process.append(Process(2, 3, 8, 2, 13, 0))
process.append(Process(3, 6, 12, 1, 15, 0))
process.append(Process(4, 0, 10, 5, 10, 0))
process.append(Process(9, 0, 10, 5, 43, 0))"""


mmu= MemoryManagementUnit('fifo', process)

mmu.load(1, 20)
print(mmu.ram.storage)
print(mmu.disk.storage)
