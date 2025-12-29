import inspect
import logging

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


# Logging
logger = logging.getLogger(__name__)

# Pandas checks
pdc.set_custom_print_fn(logger.info, print_to_stdout=False)
pdc.set_format(precision=3, use_emojis=False)
