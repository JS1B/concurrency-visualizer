import matplotlib
matplotlib.use('TkAgg')  # Use the Tkinter backend - better for threading
matplotlib.rcParams['figure.dpi'] = 80
matplotlib.rcParams['toolbar'] = 'None'

import matplotlib.pyplot as plt 
from matplotlib.widgets import Button, Slider

from src.ProcessingUnit import ProcessingUnitManager
from src.WaitingQueue import WaitingQueue, QueueVisualizer
from src.ProgressBar import ProgressBar
import src.utils as utils

# Import configuration
config = utils.load_config()

# Set up the plots
fig = plt.figure('Concurrent programming', layout='constrained', figsize=(10, 6))
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
waiting_queue = WaitingQueue(config['queue']['length'], config['queue']['size'], config['queue']['max_processing_time'])
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
button_spacing = 0.1

button_size.x0 -= button_spacing/2
addButtonAxis = fig.add_axes(list(button_size))
addButton = Button(addButtonAxis, 'Add to queue')

button_size.x0 += button_size.width + button_spacing/2
button_size.width /= 2
sliderAxis = fig.add_axes(list(button_size))
slider = Slider(sliderAxis, 'Size', 1, config['queue']['size'], valinit=config['queue']['size']//2, valstep=1)

# Configure the behavior
def add_client_callback(event):
    waiting_queue.append_to_queue(slider.val)
    
addButton.on_clicked(add_client_callback)

def plot_update_listener(id, value):
    progressBarAxis.set_bar(id, value)

manager = ProcessingUnitManager(config['threads']['count'], waiting_queue=waiting_queue, listener_callback=plot_update_listener)

# Set the callback
waiting_queue.set_on_first_item_added_callback(manager.assign_to_thread_listener)

plt.show(block=False)
manager.start()

while plt.fignum_exists(fig.number):
    # Update the plot
    fig.canvas.draw_idle()

    # Sleep for some time
    plt.pause(1/config['visualizer']['update_rate'])

manager.stop(force=True)
