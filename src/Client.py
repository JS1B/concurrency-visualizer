from matplotlib.axes import Axes
from matplotlib import patches

import random, math, time

import src.utils as utils

class Item:
    def __init__(self, time_to_process: float):
        self.time_to_process = time_to_process
        self.file_size = math.pow(time_to_process, 3)

    def get_time_to_process(self):
        return self.time_to_process

    def __str__(self):
        size_in_kb = self.file_size
        units = ["KB", "MB", "GB", "TB"]  # Add more units if needed
        index = 0

        while size_in_kb >= 1024 and index < len(units) - 1:
            size_in_kb /= 1024
            index += 1

        return f"{size_in_kb:.1f} {units[index]}"

    def __repr__(self):
        return str(self)


class Client:
    def __init__(self, id: int, itemsCount: int, maxProcessingTime: float=10, *, minProcessingTime: float=1.5):
        self.id = id

        self.items = [Item(random.random()*(maxProcessingTime-minProcessingTime)+minProcessingTime) for _ in range(itemsCount)]
        self.start_time = time.time()

    def get_item(self):
        # Return the smallest item
        return min(self.items, key=lambda x: x.time_to_process)
    
    def get_items_count(self):
        return len(self.items)
    
    def get_waiting_time(self):
        return time.time() - self.start_time
    
    def remove_item(self, item: Item):
        self.items.remove(item)

    def __str__(self):
        return f'id={self.id}, items={self.items}'

    def __repr__(self):
        return str(self)
   

class ClientVisualizer:
    def __init__(self, ax: Axes, *, colors = ['white', 'red', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray']):
        self.ax = ax

        self.position = utils.PositionType(x0=0, y0=0, width=1, height=1)

        self.color = random.choice(colors)

        self.client = None
        self.shapes = []
        self.texts = []
    
    def add_client(self, client: Client, *, x0: float=0, y0: float=0):
        self.client = client
        self.position.x0 = x0
        self.position.y0 = y0
        w = self.position.width
        h = self.position.height

        x_text = x0 + w/2
        y_text = y0 + h/2

        c = self.color
        for i, item in enumerate(client.items):
            rect = patches.Rectangle((x0+i*w, y0), w, h, facecolor=c, fill=True, linewidth=1, edgecolor='black')
            self.shapes.append(rect)
            self.ax.add_patch(rect)
            self.texts.append(self.ax.text(x_text+i*w, y_text, f'{client.id}:{item}', ha='center', va='center'))
    
    def redraw(self):
        for shape, text in zip(self.shapes, self.texts):
            shape.remove()
            text.remove()

        self.shapes = []
        self.texts = []

        for i, item in enumerate(self.client.items):
            rect = patches.Rectangle((self.position.x0+i*self.position.width, self.position.y0), self.position.width, self.position.height, facecolor=self.color, fill=True, linewidth=1, edgecolor='black')
            self.shapes.append(rect)
            self.ax.add_patch(rect)
            self.texts.append(self.ax.text(self.position.x0+i*self.position.width+self.position.width/2, self.position.y0+self.position.height/2, f'{self.client.id}:{item}', ha='center', va='center'))


class ClientFactory:
    def __init__(self, maxProcessingTime: float):
        self.clientId = 0
        self.maxProcessingTime = maxProcessingTime

    def create(self, itemsCount: int):
        self.clientId += 1
        name = f'{self.clientId}'
        return Client(name, itemsCount, self.maxProcessingTime)