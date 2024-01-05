import threading
import time

from queue import Queue, Empty

from src.ProgressBar import ProgressBar
from src.WaitingQueue import WaitingQueue

class Controller:
    def __init__(self, bars: ProgressBar, waitingQ: WaitingQueue) -> None:
        self.bars = bars

        self.queue = waitingQ
        self.returningMessagesQueue = Queue()
        # threading.Thread(target=self.process, daemon=True).start()

    def process(self):
        last_time = time.time()
        while True:
            # Get the dt
            curr_time = time.time()
            dt = curr_time - last_time
            last_time = curr_time

            item = self.assignment_queue.get()  # This will block until an item is available
            self.assign_thread()

    def assign_thread(self):
        with self.lock:
            # Assign to thread with no work based on priority
            pass
    #         min_bar = self.bars[0]
    #         for bar in self.bars:
    #             if bar.value < min_bar.value:
    #                 min_bar = bar
    #         data, qId = self.select_data_to_process()
    #         self.queues[qId].remove()
    #         min_bar.value += data['size']

    # def select_data_to_process(self):
    #     # Calculate priority based on queues' first elements - time and size

    #     def calc_size_priority(s):
    #         # s is the size of the data in seconds of processing time
    #         return math.e**(2*(-s+1))
        
    #     def calc_time_priority(t):
    #         # t is the time the data has been waiting in the queue
    #         return math.e**((-t+5)/30) + t/5
        
        # waiting_data = [d for d in self.queues[-1]]

        # priority = []
        # for d in waiting_data:
        #     if d is None:
        #         priority.append(0)
        #         continue
        #     sPrio = calc_size_priority(d['size'])
        #     tPrio = calc_time_priority(time.time() - d['time'])
        #     priority.append(sPrio + tPrio)

        # # Select data with highest priority
        # max_index = 0
        # for i in range(len(priority)):
        #     if priority[i] > priority[max_index]:
        #         max_index = i
        
        # return waiting_data[max_index], max_index
    

class ProcessingUnit:
    def __init__(self, id: int) -> None:
        self.id = id
        self.queue = Queue()
        self.lock = threading.Lock()
        self.is_processing = False
        self.thread = threading.Thread(target=self.process, daemon=True)

    def start_processing(self):
        if not self.is_processing:
            self.is_processing = True
            self.thread.start()

    def stop_processing(self):
        if self.is_processing:
            self.is_processing = False
            self.thread.join()  # This may need further control if the process can be stopped externally

    def process(self):
        while self.is_processing:
            try:
                item = self.queue.get(timeout=0.1)  # Use timeout to allow checking `is_processing` periodically
            except Empty:
                continue  # No item to process, check if still processing and try again

            last_time = time.time()
            while item.size > 0:
                time.sleep(0.1)  # Throttle the loop to avoid high CPU usage

                with self.lock:  # Ensure thread-safe modification of `item.size`
                    curr_time = time.time()
                    dt = curr_time - last_time
                    last_time = curr_time

                    item.size = max(item.size - dt, 0)

            self.queue.task_done()  # Mark the item as processed

    def update(self, item):
        self.queue.put(item)  # Add a new item to the queue for processing