import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def flatten_columns(df):
    df.columns = [
        "_".join(str(x) for x in tuple) for tuple in df.columns.to_flat_index()
    ]
    return df


def assign_with_apply(df, fn, new_cols, *args, **kwargs):
    return df.assign(
        **pd.DataFrame(
            df.apply(fn, axis=1, args=tuple(*args), **kwargs).to_list(),
            columns=new_cols,
            index=df.index,
        )
    )


def assign_from_split(df, col, sep, new_col_names, **kwargs):
    split = df[col].str.split(sep).to_list()
    new_cols_df = pd.DataFrame(split, columns=new_col_names, index=df.index, **kwargs)
    return df.assign(**new_cols_df)


def write_out(df, path, verbose=True, *args, **kwargs):
    kwargs.setdefault("index", False)
    kwargs.setdefault("sep", "\t")
    kwargs.setdefault("header", True)

    path = Path(path).resolve().relative_to(Path.cwd())

    if verbose:
        logger.info(f"Writing to {path}")

    df.to_csv(path, *args, **kwargs)

    return df
