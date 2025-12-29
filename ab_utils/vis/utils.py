import matplotlib.pyplot as plt
from statannotations.Annotator import Annotator


def rotate_tick_labels(axis, ax=None, **kwargs):
    if axis not in ("x", "y"):
        raise ValueError("axis must be 'x' or 'y'")

    kwargs.setdefault("rotation", 45)
    kwargs.setdefault("rotation_mode", "anchor")
    kwargs.setdefault("ha", "right")

    ax = ax or plt.gca()

    if axis == "x":
        ax.set_xticks(ax.get_xticks(), labels=ax.get_xticklabels(), **kwargs)
    if axis == "y":
        ax.set_yticks(ax.get_yticks(), labels=ax.get_yticklabels(), **kwargs)

    return ax

def configure_annotator(annot, *args, **kwargs):
    kwargs.setdefault("show_test_name", False)
    kwargs.setdefault("text_format", "simple") # Use "full" for exact P values below the threshold
    kwargs.setdefault("pvalue_thresholds", [[1e-16, "1e-16"]])
    kwargs.setdefault("pvalue_format_string", "{:.3g}")
    kwargs.setdefault("p_capitalized", True)
    kwargs.setdefault("p_separators", ("",""))
    kwargs.setdefault("loc", "outside")
    kwargs.setdefault("line_height", 0)
    kwargs.setdefault("line_width", 1)

    return annot.configure(*args, **kwargs)
