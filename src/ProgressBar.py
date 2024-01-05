from matplotlib.axes import Axes

class ProgressBar:
    def __init__(self, ax: Axes, name: str, count: int):
        ax.set_title('Progress Bar')

        ax.set_ylim([0, 100])
        ax.set_yticks([0, 10, 25, 50, 100])
        ax.set_ylabel('Processing [s]')

        x_range = range(1, count+1)
        ax.set_xlim([0, count+1])
        ax.set_xticks(x_range)
        ax.set_xticklabels([f'{name} {i}' for i in x_range])

        v = [0 for _ in x_range]
        self.bar = ax.bar(list(x_range), v, color='cyan', edgecolor='black')
        self.ax = ax

    def set_bar(self, index, v):
        self.bar[index].set_height(v)
