from matplotlib.axes import Axes

from src.Client import ClientFactory, ClientVisualizer, Client, Item

class WaitingQueue:
    def __init__(self, max_clients: int, max_items_per_client: int, maxProcessingTime: float=100, *, on_new_client_callback=None, on_item_removal_callback=None, on_first_item_added_callback=None):
        self.clients_queue = []
        self.client_factory = ClientFactory(maxProcessingTime)
        self.max_clients = max_clients
        self.max_items_per_client = max_items_per_client

        self.on_new_client_callback = on_new_client_callback
        self.on_item_removal_callback = on_item_removal_callback
        self.on_first_item_added_callback = on_first_item_added_callback
        
    def set_on_new_client_callback(self, callback):
        self.on_new_client_callback = callback

    def set_on_item_removal_callback(self, callback):
        self.on_item_removal_callback = callback

    def set_on_first_item_added_callback(self, callback):
        self.on_first_item_added_callback = callback

    def append_to_queue(self, itemsCount: int):
        if len(self.clients_queue) >= self.max_clients:
            return
        
        was_empty = len(self.clients_queue) == 0
        client = self.client_factory.create(itemsCount)
        self.clients_queue.append(client)
        print(self.clients_queue)

        if self.on_new_client_callback:
            self.on_new_client_callback(client)

        if was_empty and self.on_first_item_added_callback:
            self.on_first_item_added_callback()

    def get_item_from_queue(self):
        # Get the client with the smallest item
        if len(self.clients_queue) == 0:
            return None
        
        client = min(self.clients_queue, key=lambda c: c.get_item().size)

        # Remove item from client
        item = client.get_item()
        client.remove_item(item)

        # Remove client if empty
        if len(client.items) == 0:
            self.clients_queue.remove(client)

        print(self.clients_queue)

        # Invoke callback with client and item
        if self.on_item_removal_callback:
            self.on_item_removal_callback(client, item)
        return item
        

class QueueVisualizer:
    def __init__(self, ax: Axes, waiting_queue: WaitingQueue):
        self.ax = ax
        
        waiting_queue.set_on_item_removal_callback(self.remove_from_queue)
        waiting_queue.set_on_new_client_callback(self.append_to_queue)
        self.waiting_queue = waiting_queue
        
        self.configure_axes()

        self.client_visualizers = []
    
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
        new_cv = ClientVisualizer(self.ax)
        
        # Get the y position of the first blank space #TODO
        y = -1
        for cv in self.client_visualizers:
            y = min(y, cv.position.y0 - cv.position.height)
            if cv.position.y0 + cv.position.height < y:
                break

        if y < self.ax.get_ylim()[0]:
            return
        
        new_cv.add_client(client, y0=y)
        self.client_visualizers.append(new_cv)

    def remove_from_queue(self, client: Client, item: Item):
        for cv in self.client_visualizers:
            if cv.client == client:
                if len(cv.client.items) == 0:
                    self.redraw()
                    self.client_visualizers.remove(cv)
                break
        self.redraw()

    def redraw(self):
        for cv in self.client_visualizers:
            cv.redraw()