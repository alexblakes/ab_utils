import inspect
import logging
import sys
from pathlib import Path

import pandas as pd
import pandas_checks as pdc


def get_calling_fn(*ignore: str) -> str | None:
    """Return the name of the calling function.

    This function skips frames that originate from this module (so helpers like
    `get_prefix` aren't returned) and common wrapper names like
    `pipe` (pandas) by default.
    """
    default_ignore = {"pipe"}
    ignore_set = set(ignore) | default_ignore

    for frameinfo in inspect.stack()[1:]:
        # skip functions in this module
        module_name = frameinfo.frame.f_globals.get("__name__", "")
        if module_name == __name__:
            continue

        # skip names in `ignore`
        name = frameinfo.function
        if name not in ignore_set:
            return name

    return None

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
    file_log = Path(snakemake.log[0]).resolve()
except (ImportError):
    logger.info("Running outside Snakemake. Logging to stderr only.")
except (IndexError):
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
