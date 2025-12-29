import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def boxplot(
    dfg,
    col,
    colors,
    ax=None,
    label_n=True,
    min_n_box=5,
    min_n_alpha=25,
    scatter_kwargs=None,
    boxplot_kwargs=None,
):
    ax = ax or plt.gca()

    if scatter_kwargs is None:
        scatter_kwargs = {}

    scatter_kwargs.setdefault("lw", 0)
    scatter_kwargs.setdefault("alpha", 0.3)

    if boxplot_kwargs is None:
        boxplot_kwargs = {}

    boxplot_kwargs.setdefault("vert", True)
    boxplot_kwargs.setdefault("whis", [2.5, 97.5])
    boxplot_kwargs.setdefault("widths", [0.5])
    boxplot_kwargs.setdefault("showfliers", False)
    boxplot_kwargs.setdefault("showmeans", True)
    boxplot_kwargs.setdefault("medianprops", dict(color="black"))
    boxplot_kwargs.setdefault(
        "meanprops",
        dict(
            color="black",
            marker="o",
            mew=1,
            markeredgecolor="black",
            markerfacecolor="white",
            markersize=3,
        ),
    )

    for (i, (group, data)), color in zip(enumerate(dfg), colors):
        y = data[col]
        n = len(y)
        jitter = np.random.uniform(-0.15, 0.15, size=n)
        x = i + jitter
        label = group

        if label_n:
            label += f"\n(N={n})"

        if n < min_n_alpha:
            scatter_kwargs.update(alpha=1)

        ax.scatter(x, y, color=color, **scatter_kwargs)

        if n < min_n_box:
            # Plot an empty boxplot
            ax.boxplot(
                y,
                positions=[i],
                labels=[label],
                showbox=False,
                showcaps=False,
                showmeans=False,
                whiskerprops=dict(linestyle="None"),
                medianprops=dict(linestyle="None"),
            )
        else:
            ax.boxplot(y, positions=[i], labels=[label], **boxplot_kwargs)

    return ax


def grouped_vertical_bar(
    df,
    cluster_column,
    bar_column,
    data_column,
    err_columns=None,
    bar_label_fmt=None,
    colors=None,
    ax=None,
    *args,
    **kwargs,
):
    ax = ax or plt.gca()

    dfg = df.groupby(bar_column, sort=False)
    n_clusters = len(dfg)

    if colors is None:
        colors = [[]] * n_clusters

    for (i, (name, data)), color in zip(enumerate(dfg), colors):
        n_bars = len(data)
        labels = data[cluster_column]
        y = data[data_column]
        left_bar_positions = np.arange(n_bars)
        bar_width = 1 / (n_clusters + 1)
        offset = bar_width * i
        bar_positions = (left_bar_positions + offset) - (bar_width / 2)

        err_values = None
        if err_columns:
            err_values = data[err_columns].values.transpose()
            print(err_values)

        if color:
            kwargs.update(color=color)

        bars = ax.bar(
            bar_positions,
            height=y,
            width=bar_width,
            label=name,
            yerr=err_values,
            *args,
            **kwargs,
        )
        if not bar_label_fmt is None:
            ax.bar_label(bars, fmt=bar_label_fmt)

    tick_positions = left_bar_positions + (bar_width * (n_clusters - 2) / 2) #- (bar_width/2)
    ax.set_xticks(tick_positions, labels=labels)

    return ax
