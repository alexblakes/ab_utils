import matplotlib.pyplot as plt
from matplotlib import cm
from importlib.resources import files

from .plot import boxplot, grouped_vertical_bar
from .utils import rotate_tick_labels, configure_annotator
from .color import adjust_alpha

# Colours
RED = cm.Reds(0.8)
BLUE = cm.Blues(0.8)

plt.style.use("ab_utils.vis.style.default")
