import matplotlib
matplotlib.use('TkAgg')  # Use the Tkinter backend - better for threading
import matplotlib.pyplot as plt 
from matplotlib.widgets import Button, TextBox
import time

from src.ProcessingUnit import ProcessingUnitManager
from src.WaitingQueue import WaitingQueue, QueueVisualizer
from src.ProgressBar import ProgressBar
import src.utils as utils

# Import configuration
config = utils.load_config('config.yaml')

# Set up the plots
fig = plt.figure('Concurrent programming', layout='constrained')
fig.suptitle(config['visualizer']['title'], fontsize=config['visualizer']['title_font_size'])


axd = fig.subplot_mosaic(
    [
        ['progress_bar', 'waiting_queue'],
        ['controls', 'waiting_queue']
    ],
    width_ratios=[5, 2],
    height_ratios=[10, 1]
)

# Set up the progress bars axis
progressBarAxis = ProgressBar(axd['progress_bar'], 'Thread', config['threads']['count'])

# Set up the waiting queue axis
waiting_queue = WaitingQueue(config['queue']['length'], config['queue']['size'])
waiting_queue_visualizer = QueueVisualizer(axd['waiting_queue'], waiting_queue)

# Set up the controls axis
controlsAxis = axd['controls']
controlsAxis.set_title('Controls')
controlsAxis.set_axis_off()

button_size = utils.PositionType(
    x0=controlsAxis.get_position().x0 + 0.1,
    y0=controlsAxis.get_position().y0 - 0.1 * (controlsAxis.get_title != ''), # 0.1 is the title height
    width=controlsAxis.get_position().width/2,
    height=controlsAxis.get_position().height
)
button_spacing = 0.04

button_size.x0 -= button_spacing/2
addButtonAxis = fig.add_axes(list(button_size))
addButton = Button(addButtonAxis, 'Add to queue')

button_size.x0 += button_size.width + button_spacing/2
button_size.width /= 2
textBoxAxis = fig.add_axes(list(button_size))
textBox = TextBox(textBoxAxis, '', initial='1', textalignment='center')

def on_click(event):
    try:
        val = int(float(textBox.text))
    except ValueError:
        textBox.color = 'red'
        return
    else:
        textBox.color = 'white'
    waiting_queue.append_to_queue(val)
    client = waiting_queue.clients_queue[-1]
    waiting_queue_visualizer.append_to_queue(client)

    
addButton.on_clicked(on_click)
# textBox.label.set_visible(False)

def plot_update_listener(id, value):
    progressBarAxis.set_bar(id, value)

def finished_thread_listener():
    client = waiting_queue.remove_from_queue()
    if client:
        item = client.items.pop(0)
        manager.add_task(item.size)

manager = ProcessingUnitManager(config['threads']['count'], listener_callback=plot_update_listener)

plt.show(block=False)
manager.start()

while plt.fignum_exists(fig.number):
    # Update the plot
    fig.canvas.draw_idle()

    # Sleep for some time
    plt.pause(0.016)

manager.stop(force=True)
