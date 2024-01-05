import random

class ClientFactory:
    def __init__(self, maxProcessingTime: float):
        self.clientId = 0
        self.maxProcessingTime = maxProcessingTime

    def create(self, itemsCount: int):
        self.clientId += 1
        name = f'{self.clientId}'
        return Client(name, itemsCount, self.maxProcessingTime)

class Client:
    def __init__(self, id: int, itemsCount: int, maxProcessingTime: float=1):
        self.id = id
        self.items = [Item(random.random()*maxProcessingTime) for _ in range(itemsCount)]

    def __str__(self):
        return f'{self.name}: {self.items}'

    def __repr__(self):
        return str(self)
    

class Item:
    def __init__(self, size: float):
        self.size = size

    def __str__(self):
        return f'{self.size:.1f}'

    def __repr__(self):
        return str(self)
