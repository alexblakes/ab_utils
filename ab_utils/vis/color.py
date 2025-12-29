from matplotlib import colors as mc

def adjust_alpha(color, alpha):
    return mc.to_rgba(color, alpha)
