import pandas as pd

def flatten_columns(df):
    df.columns = ["_".join(str(x) for x in tuple) for tuple in df.columns.to_flat_index()]
    return df

def assign_with_apply(df, fn, new_cols, *args, **kwargs):
    return df.assign(
        **pd.DataFrame(
        df.apply(fn, axis=1, args=tuple(*args), **kwargs).to_list(),
        columns=new_cols,
        index=df.index
        )
    )