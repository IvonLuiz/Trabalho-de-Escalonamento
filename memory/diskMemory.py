class Disk:
    def __init__(self, storage, storageLeft) -> None:
        self.storage= [0]*storage #Será 250
        self.storageLeft= storage #Será 250

    def storeItem(self, processId, numberOfPages):
        if numberOfPages<= self.storageLeft:
            pagesWritten= 0
            currentPage= 0
            while pagesWritten<numberOfPages:
                if self.storage[currentPage] == 0:
                    self.storage[currentPage]= processId
                    pagesWritten+= 1

                currentPage+= 1
            self.storageLeft+= pagesWritten*-1
        else:
            print("Operation failed, disk is full.")


    def removeItem(self, processId, numberOfPages):
        currentPage= 0
        pagesRemoved= 0
        while pagesRemoved<numberOfPages:
            if self.storage[currentPage] == processId:
                self.storage[currentPage]= 0
                pagesRemoved+= 1

            
            currentPage+= 1
        self.storageLeft+= pagesRemoved
        return pagesRemoved