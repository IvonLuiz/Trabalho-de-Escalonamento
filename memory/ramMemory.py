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


