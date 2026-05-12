import inspect
import logging
from pathlib import Path

import pandas as pd
import pandas_checks  # noqa: F401

logger = logging.getLogger(__name__)


def flatten_columns(df):
    df.columns = ["_".join(map(str, col)) for col in df.columns.to_flat_index()]
    return df


def assign_with_apply(df, fn, new_cols, *args, **kwargs):
    return df.assign(
        **pd.DataFrame(
            df.apply(fn, axis=1, args=args, **kwargs),
            columns=new_cols,
            index=df.index,
        )
    )


def assign_from_split(df, col, sep, new_col_names, **kwargs):
    return df.assign(
        **pd.DataFrame(
            df[col].str.split(sep), columns=new_col_names, index=df.index, **kwargs
        )
    )


def read(path, verbose=True, **kwargs):
    kwargs.setdefault("sep", "\t")

    path = Path(path).resolve()
    try:
        path = path.relative_to(Path.cwd())
    except ValueError:
        pass

    if verbose:
        logger.info(f"Reading from {path}")

    return pd.read_csv(path, **kwargs).check.nrows(check_name=f"Input lines in {path.name}")


def write(df, path, verbose=True, **kwargs):
    kwargs.setdefault("index", False)
    kwargs.setdefault("sep", "\t")

    path = Path(path).resolve()
    try:
        path = path.relative_to(Path.cwd())
    except ValueError:
        logger.warning(
            f"Path '{path}' is not relative to the current working directory."
            "Using absolute path instead."
        )
        pass

    if verbose:
        logger.info(f"Writing to {path}")

    df.check.nrows(check_name="Output lines").to_csv(path, **kwargs)

    return df
<<<<<<< HEAD

def add_global(df, var_name):
    inspect.currentframe().f_back.f_globals[var_name] = df
    return df
=======
>>>>>>> parent of 9672e9e (Add global method)
