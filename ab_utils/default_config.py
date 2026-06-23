"""Opt-in default configuration for ab_utils.

Importing this module applies Alex's preferred global configuration for
logging, pandas / pandas_checks, and matplotlib. It is *not* loaded by
``import ab_utils`` so that importing the package has no side effects. Apply it
explicitly when you want it::

    from ab_utils import default_config  # noqa: F401

All configuration runs once, at import time.
"""

import logging
import sys
from pathlib import Path

from matplotlib import cm
import matplotlib.pyplot as plt
import pandas as pd
import pandas_checks as pdc

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers.clear()

main_module = sys.modules.get("__main__")
main_file = getattr(main_module, "__file__", "__main__")
file_name = Path(main_file).name

FORMAT = f"[%(asctime)s] {file_name} %(levelname)s || %(message)s"
formatter = logging.Formatter(FORMAT, style="%")

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

logger.addHandler(stream_handler)

# Set up logging via Snakemake if possible
try:
    from snakemake.script import snakemake

    logger.info("Running from Snakemake.")
    file_log = Path(snakemake.log[0])
except ImportError:
    logger.info("Running outside Snakemake. Logging to stderr only.")
except IndexError:
    logger.warning("No Snakemake log file detected. Logging only to stderr.")
else:
    file_handler = logging.FileHandler(file_log, mode="w")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.info(f"Logging to stderr and '{file_log}' via Snakemake")


# Pandas checks
pdc.set_format(precision=4, use_emojis=False)

# In terminal, send pandas checks to the logger instead of stdout
if pd.core.config_init.is_terminal():
    pdc.set_custom_print_fn(logger.info, print_to_stdout=False)

# Pandas
pd.set_option("display.precision", 4)

# Matplotlib
plt.style.use("ab_utils.vis.style.default")

# Colours
RED = cm.Reds(0.8)
BLUE = cm.Blues(0.8)
    