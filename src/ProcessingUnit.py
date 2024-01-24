import threading
import time

from queue import Queue, Empty

class ProcessingUnit:
    def __init__(self, id: int, listener_callback=None):
        self.id = id

        self.listener_callback = listener_callback

        self.queue = Queue()
        self.thread = threading.Thread(target=self.process, daemon=True)

        self.stop_signal = threading.Event()

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
                time.sleep(0.1)  # Simulate work by sleeping for 1 second
                value = max(value - 0.1, 0)  # Update value

                if self.listener_callback:
                    self.listener_callback(self.id, value)  # Notify listener when processing is complete
            
            print(f"Processing unit {self.id} finished processing.")
            self.queue.task_done()  # Mark the task as done
            
    def add_task(self, value):
        self.queue.put(value)


class ProcessingUnitManager:
    def __init__(self, count: int, listener_callback=None):
        self.units = [ProcessingUnit(i, listener_callback) for i in range(count)]

    def start(self):
        for unit in self.units:
            unit.start()

    def stop(self, force=False):
        for unit in self.units:
            unit.stop(force)

    def add_task(self, value):
        # Add the task to the unit with the shortest queue
        min_unit = min(self.units, key=lambda unit: unit.queue.qsize())
        min_unit.add_task(value)
