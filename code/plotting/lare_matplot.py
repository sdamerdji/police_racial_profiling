import matplotlib.pyplot as plt
import numpy as np


def basic_plot(params):
    # nothing fancy, just plot it
    if params.type == "loglog":
        plt.loglog(params.xax, params.yax, '.')
    elif params.type == "log":
        plt.semilog(params.xax, params.yax, '.')
    elif params.type == "bar":
        plt.bar(params.xax, params.yax)
    else:
        plt.plot(params.xax, params.yax, '.')

    plt.xlabel(params.xlabel)
    plt.ylabel(params.ylabel)
    plt.title(params.title)
    plt.show()


def single_bar(pd_series, name, fig, num_bars, bar_num):
    if name == "age":
        age_bins = [10 * x for x in range(10)]
        age_hist = np.histogram(pd_series.values, bins=age_bins)
        data = age_hist[0]
        category_names = ["{}-{}".format(age_bins[i], age_bins[i + 1]) for i in range(len(age_bins) - 1)]
    else:
        counts = pd_series.value_counts()
        category_names = counts.keys()
        data = counts.values

    labels = [name]
    data_cum = data.cumsum()
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, len(data)))

    ax = plt.subplot(num_bars, 1, bar_num)
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.max(sum(data), 0))

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[i]
        starts = data_cum[i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.8,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, labels=[colname], label_type='center', color=text_color, rotation=0)


def plot_descriptive_bars(df):
    keys = ["race", "age", "call_for_service", "reason_for_stop", "result", "gender", "evidence_found", "actions_taken"]
    fig = plt.subplots(len(keys), 1)
    for key in keys:
        single_bar(df[key], key, fig, 1, 1)
    plt.show()
