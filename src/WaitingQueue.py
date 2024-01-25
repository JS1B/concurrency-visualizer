from matplotlib import patches
from matplotlib.axes import Axes

from src.Client import ClientFactory, ClientVisualizer, Client

class WaitingQueue:
    def __init__(self, max_clients: int, max_items_per_client: int, maxProcessingTime: float=100, on_new_client_callback=None):
        self.clients_queue = []
        self.client_factory = ClientFactory(maxProcessingTime)
        self.max_clients = max_clients
        self.max_items_per_client = max_items_per_client

        self.on_new_client_callback = on_new_client_callback
        
    def append_to_queue(self, value: int):
        if len(self.clients_queue) >= self.max_clients:
            return
        
        was_empty = len(self.clients_queue) == 0
        client = self.client_factory.create(value)
        self.clients_queue.append(client)
        if was_empty and self.on_new_client_callback:
            self.on_new_client_callback()

        print(self.clients_queue)
    
    def remove_from_queue(self, client_id):
        client = next((c for c in self.clients_queue if c.id == client_id), None)
        if client:
            self.clients_queue.remove(client)
        return client
        

class QueueVisualizer:
    def __init__(self, ax: Axes, waiting_queue: WaitingQueue):
        self.ax = ax
        self.waiting_queue = waiting_queue
        
        self.configure_axes()

        self.client_visualizers = []

        self.colors = ['white', 'red', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray']
    
    def configure_axes(self):
        xySize = self.waiting_queue.max_items_per_client, self.waiting_queue.max_clients
        self.ax.set_title('Waiting Queue')

        self.ax.set_ylim(-int(abs(xySize[1])), 0)
        self.ax.autoscale(False)
        # self.ax.set_yticks([])

        self.ax.set_xlim(0, int(abs(xySize[0])))
        # self.ax.set_xticks([])

        # self.ax.axis('off')
        
    def append_to_queue(self, client: Client):
        cv = ClientVisualizer(self.ax)
        y = -len(self.waiting_queue.clients_queue)

        if y < self.ax.get_ylim()[0]:
            return
        
        cv.add_client(client, y0=y)
        self.client_visualizers.append(cv)
    
    def remove_client(self, client_id):
        client = self.waiting_queue.remove_from_queue(client_id)
        if client:
            for rect in client.rects:
                rect.remove()
            for text in client.texts:
                text.remove()
            self.ax.figure.canvas.draw()