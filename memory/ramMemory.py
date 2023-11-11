class Ram:
    def __init__(self, storage, storageLeft) -> None:
        self.storage= [0]*storage #Será 50
        self.storageLeft= storageLeft #Será 50

    def write(self, processId, overwriteID, numberOfPages):
        pagesWritten= 0
        currentPage= 0
        #Temos espaço suficiente para colocar todo o processo na ram
        if numberOfPages<= self.storageLeft:  
            while pagesWritten<numberOfPages:
                if self.storage[currentPage] == 0:
                    self.storage[currentPage]= processId
                    pagesWritten+= 1

                currentPage+= 1
            self.storageLeft+= pagesWritten*-1
            return pagesWritten
        

        else:
            if self.storageLeft>0: #Existe algum espaço livre
                while currentPage<(len(self.storage)): 
                    if self.storage[currentPage] == 0:
                        self.storage[currentPage]= processId
                        pagesWritten+= 1

                    currentPage+= 1
                self.storageLeft+= pagesWritten*-1
                return pagesWritten
            
            #Operação de Overwrite é necessária pois a ram está cheia
            else:
                while pagesWritten<numberOfPages:
                    if currentPage>(len(self.storage)-1): #Out of bounds
                        break
                    if self.storage[currentPage] == overwriteID:
                        self.storage[currentPage]= processId
                        pagesWritten+= 1

                    currentPage+= 1
                return pagesWritten


""""ram= Ram(50,50)
print(ram.storage)
print(ram.storageLeft)

written= ram.write(2, 0, 10)
print(ram.storage)
print(ram.storageLeft)
print(written)

written= ram.write(5, 0, 15)
print(ram.storage)
print(ram.storageLeft)
print(written)

written= ram.write(4, 0, 20)
print(ram.storage)
print(ram.storageLeft)
print(written)

#ram estará semi cheia
written= ram.write(8, 0, 20)
print(ram.storage)
print(ram.storageLeft)
print(written)

#ram está cheia
spaceNeeded= 33
removalQueue= [4, 2, 5, 8]
pages= [20, 10, 15, 20]
while spaceNeeded>0:
    written= ram.write(9, removalQueue[0], spaceNeeded)
    spaceNeeded-= written
    pages[0]-=written
    if pages[0] <= 0:
        removalQueue.pop(0)
        pages.pop(0)

    print(f'removal queue: {removalQueue}')
    print(f'pages: {pages}')
    print(ram.storage)
    print(ram.storageLeft)
    print(written)

removalQueue.append(9)
pages.append(33)
print(f'removal queue: {removalQueue}')
print(f'pages: {pages}')"""
