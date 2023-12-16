import matplotlib
matplotlib.use('TkAgg')  # Use the Tkinter backend - better for threading
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
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
            time.sleep(0.1)  # Update every 0.01 seconds

    def stop(self):
        self.running = False

class VisualQueue:
    def __init__(self, ax, max_size=5):
        self.ax = ax
        self.max_size = max_size
        self.queue = []
        self.rects = []
        self.texts = []
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, max_size)
        self.ax.axis('off')

    def add(self, value):
        if len(self.queue) < self.max_size:
            self.queue.append(value)
            self.update_visual()

    def remove(self):
        if self.queue:
            self.queue.pop(0)
            self.update_visual()

    def update_visual(self):
        # Clear previous rectangles and texts
        for rect in self.rects:
            rect.remove()
        for text in self.texts:
            text.remove()
        self.rects.clear()
        self.texts.clear()

        # Draw new rectangles and texts
        for i, value in enumerate(self.queue):
            if i < len(self.rects):
                # Reuse existing rectangle and text
                self.rects[i].set_height(1)
                self.texts[i].set_text(str(value))
            else:
                # Create new rectangle and text
                rect = patches.Rectangle((0, i), 1, 1, edgecolor='black', facecolor='skyblue')
                self.ax.add_patch(rect)
                self.rects.append(rect)
                text = self.ax.text(0.5, i + 0.5, str(value), ha='center', va='center', fontsize=12)
                self.texts.append(text)

def on_click(event, q):
    q.add(f"t {0}, size {0}")

# Load the config
config = utils.load_config()

# Set up the plot
threads_count = config['threading']['count']
queue_count = config['queue']['count']
fig, axs = plt.subplots(2, max(threads_count, queue_count), figsize=(10, 8))
# fig.tight_layout()
fig.suptitle(config['visualizer']['title'], fontsize=config['visualizer']['title_font_size'])

# Ensure axs is a 2D array
if threads_count == 1 or queue_count == 1:
    axs = axs.reshape(2, -1)

# Set up the bars and queues
bars = []
queues = []
buttons = []

for i in range(max(threads_count, queue_count)):
    if i < threads_count:
        # Setup for bars
        axs[0, i].set_ylim(config['visualizer']['y_lim'])
        axs[0, i].set_yticks([])
        bar = Bar(i, axs[0, i])
        bars.append(bar)

    if i < queue_count:
        # Setup for queues
        queue = VisualQueue(axs[1, i])
        queues.append(queue)

        # Setup for buttons
        button_ax = plt.axes([0.15 + 0.2 * i, 0.04, 0.12, 0.05])
        button = Button(button_ax, f"Add to queue {i}")
        button.on_clicked(lambda event, q=queue: on_click(event, q))
        buttons.append(button)

if threads_count > 0:
    axs[0, 0].set_yticks(config['visualizer']['y_ticks'])
    axs[0, 0].set_ylabel(config['visualizer']['y_label'])

    axs[1, 0].set_ylabel("Queues")

# Start bar update threads
for bar in bars:
    bar.start()

# Display the plot
plt.show()

# Stop the threads when the plot window is closed
for bar in bars:
    bar.stop()
