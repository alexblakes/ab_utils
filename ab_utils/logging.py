import inspect
import logging
from pathlib import Path

import pandas as pd
import pandas_checks as pdc

FORMAT = "[{asctime}] [{levelname}] || {message}"

logging.basicConfig(format=FORMAT, style="{", level=logging.INFO)
logger = logging.getLogger()


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


# Set up logging via Snakemake if possible
try:
    from snakemake.script import snakemake

    file_log = Path(snakemake.log[0]).resolve()
except (ImportError, IndexError):
    logger.info("No Snakemake log file detected. Logging to stderr only.")
else:
    file_handler = logging.FileHandler(file_log, mode="w")
    file_handler.setFormatter(logging.Formatter(FORMAT, style="{"))
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.info(f"Logging to stderr and '{file_log}' via Snakemake")


# Pandas checks
pdc.set_format(precision=4, use_emojis=False)

if not pd.core.config_init.is_terminal():
    # Use default print function in interactive envs
    pdc.set_custom_print_fn(None, print_to_stdout=True)
else:
    # Use logger in terminal
    pdc.set_custom_print_fn(logger.info, print_to_stdout=False)
