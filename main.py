import matplotlib
matplotlib.use('TkAgg')  # Use the Tkinter backend - better for threading
import matplotlib.pyplot as plt 
from matplotlib.widgets import Button, TextBox
import time

from src.Controller import Controller
from src.WaitingQueue import WaitingQueue
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
waitingQueueAxis = WaitingQueue(axd['waiting_queue'], (config['queue']['size'], config['queue']['length']))

# waitingQueueAxis.set_axis_off()

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
textBox = TextBox(textBoxAxis, '', initial='Size', textalignment='center')

def on_click(event):
    try:
        val = int(float(textBox.text))
    except ValueError:
        textBox.color = 'red'
        return
    else:
        textBox.color = 'white'
    waitingQueueAxis.append_to_queue(val)
    
addButton.on_clicked(on_click)
# textBox.label.set_visible(False)

controller = Controller(progressBarAxis, waitingQueueAxis)

plt.show(block=False)

while plt.fignum_exists(fig.number):

    controller.process()

    # Update the plot
    fig.canvas.draw_idle()

    # Sleep for the remaining time
    plt.pause(0.016)
