import matplotlib.pyplot as plt


def basic_plot(params):
    # nothing fancy, just plot it
    if params.scale == "loglog":
        plt.loglog(params.xax, params.yax)
    elif params.scale == "log":
        plt.semilog(params.xax, params.yax)
    else:
        plt.plot(params.xax, params.yax)

    plt.xlabel(params.xlabel)
    plt.ylabel(params.ylabel)
    plt.title(params.title)
