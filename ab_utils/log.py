import inspect


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
