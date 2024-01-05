from matplotlib import patches
from matplotlib.axes import Axes
import random

from src.Client import ClientFactory, Client

class WaitingQueue:
    def __init__(self, ax: Axes, xySize: tuple, maxProcessingTime: float=100):
        if len(xySize) != 2:
            raise ValueError('xySize must be a tuple of length 2')
        
        ax.set_title('Waiting Queue')

        ax.set_ylim(-int(abs(xySize[1])), 0)
        ax.autoscale(False)
        ax.set_yticks([])

        ax.set_xlim(0, int(abs(xySize[0])))
        ax.set_xticks([])

        ax.axis('off')
        self.ax = ax

        self.queue = []
        self.clientId = 0

        self.element_height = 1
        self.element_width = 1

        self.colors = ['white', 'red', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray']
        self.clientFactory = ClientFactory(maxProcessingTime)
        
    def append_to_queue(self, value: int):
        if value < self.ax.get_xlim()[0]+1:
            value = int(self.ax.get_xlim()[0])+1

        if value > self.ax.get_xlim()[1]:
            value = int(self.ax.get_xlim()[1])

        client = self.clientFactory.create(value)

        self.queue.append(client)
        y = len(self.queue) * -self.element_height

        if y < self.ax.get_ylim()[0]:
            return

        c = self.colors[y % len(self.colors)]
        for i, item in enumerate(client.items):
            self.add_box_with_text(i, y, self.element_width, self.element_height, f'{client.id}: {item}', color=c)
    
    def pop_from_queue(self):
        if len(self.queue) == 0:
            return
        
        client = self.queue.pop(0)
        return client
        # y = len(self.queue) * -self.element_height

        # if y < self.ax.get_ylim()[0]:
        #     return

        # for i, val in enumerate(client.values):
        #     self.add_box_with_text(i, y, self.element_width, self.element_height, f'{client.name}: {val}')

    def add_box_with_text(self, x, y, width, height, text, color='white'):
        # Create a rectangle patch and add it to the axis
        rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor='black', facecolor=color)
        self.ax.add_patch(rect)
        
        # Add text at the center of the rectangle
        text_x = x + width / 2
        text_y = y + height / 2
        self.ax.text(text_x, text_y, text, ha='center', va='center')
        