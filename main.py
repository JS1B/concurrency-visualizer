import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend to prevent segmentation fault
import matplotlib.pyplot as plt
import threading
import time
import utils

class Bar:
    def __init__(self, id, ax, initial_value=10):
        self.id = id
        self.ax = ax
        self.value = initial_value
        self.lock = threading.Lock()
        self.bar = ax.bar(f"Thread {id}", initial_value)
        self._last_time = time.time()
        self.running = True

    def start(self):
        threading.Thread(target=self.update_plot, daemon=True).start()

    def update_plot(self):
        while self.running:
            with self.lock:
                curr_time = time.time()
                elapsed = curr_time - self._last_time
                self._last_time = curr_time

                self.value = max(0, self.value - elapsed)

                # Thread-safe way to update the plot
                self.ax.figure.canvas.draw_idle()
                self.bar[0].set_height(self.value)
            time.sleep(0.01)  # Update every 0.01 seconds

    def stop(self):
        self.running = False

# Load the config
config = utils.load_config()

# Set up the plot
threads_count = config['threading']['count']
fig, axs = plt.subplots(1, threads_count)

# Set up the bars
for ax in axs:
    ax.set_ylim(0, 100)
    ax.set_yticks([])

axs[0].set_yticks([0, 10, 50, 100])
axs[0].set_ylabel("Progress [s]")

bars = [Bar(i, axs[i]) for i in range(threads_count)]

# Start bar update threads
for bar in bars:
    bar.start()

# Display the plot
plt.show()

# Stop the threads when the plot window is closed
for bar in bars:
    bar.stop()
