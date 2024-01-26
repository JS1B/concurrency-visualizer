import threading
import time

from queue import Queue, Empty
from src.WaitingQueue import WaitingQueue

class ProcessingUnit:
    def __init__(self, id: int, listener_callback=None, idle_callback=None):
        self.id = id

        self.listener_callback = listener_callback

        self.queue = Queue()
        self.thread = threading.Thread(target=self.process, daemon=True)

        self.stop_signal = threading.Event()

        self.idle_callback = idle_callback

    def start(self):
        if not self.thread.is_alive():
            print(f"Starting processing unit {self.id}.")
            self.thread.start()

    def stop(self, force=False):
        self.stop_signal.set()
        if force:
            # Clear all remaining items in the queue
            while not self.queue.empty():
                try:
                    self.queue.get_nowait()
                    self.queue.task_done()
                except Empty:
                    continue
        self.thread.join()

    def process(self):
        while not self.stop_signal.is_set():
            try:
                value = self.queue.get(timeout=0.1)
                print(f"Processing unit {self.id} got value {value}.")
            except Empty:
                continue  # No item to process, check if still processing and try again

            while value > 0 and not self.stop_signal.is_set():
                time.sleep(0.1)  # Simulate work by sleeping for .1 second
                value = max(value - 0.1, 0)  # Update value

                if self.listener_callback:
                    self.listener_callback(self.id, value)  # Notify listener when processing
            
            print(f"Processing unit {self.id} finished processing.")

            if self.idle_callback:
                self.idle_callback()
            self.queue.task_done()  # Mark the task as done
            
    def add_task(self, value):
        self.queue.put(value)


class ProcessingUnitManager:
    def __init__(self, count: int, waiting_queue: WaitingQueue, listener_callback=None):
        self.waiting_queue = waiting_queue
        self.units = [ProcessingUnit(i, listener_callback, self.assign_to_thread_listener) for i in range(count)]

    def start(self):
        for unit in self.units:
            unit.start()

    def stop(self, force=False):
        for unit in self.units:
            unit.stop(force)

    def assign_to_thread(self, unit: ProcessingUnit):
        # print(f"Assigning to unit {unit.id}.")
        clients = self.waiting_queue.get_clients_from_queue()
        if not clients:
            return
        
        # The smaller the value, the higher the priority
        client_item = [(client, client.get_item()) for client in clients]

        # Calculate the priority based on the item processing time and the client start time
        # The longer the waiting time, the higher the priority
        # The smaller the item processing time, the higher the priority
        client_item = [(client, item, item.time_to_process / (time.time() - client.start_time)) for client, item in client_item]

        # Get the client with the highest priority
        client, item, _ = min(client_item, key=lambda x: x[2])

        # Remove item from client
        self.waiting_queue.remove_from_queue(client, item)

        if item:
            unit.add_task(item.time_to_process)

    def assign_to_thread_listener(self):
        for unit in self.units:
            if unit.queue.empty():
                self.assign_to_thread(unit)
                continue
