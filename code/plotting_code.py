import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def make_quadrant_chart(x, y, **kwargs):
    '''
    Makes the classic four quadrant chart.
    '''

    # Optional arguments for customization
    figsize = kwargs.pop('figsize', (9, 9))
    bm = 1 + kwargs.pop('bounds_multiplier', 0.1)
    xlabel = kwargs.pop('xlabel', None)
    ylabel = kwargs.pop('ylabel', None)
    highlight_quadrant = kwargs.pop('highlight_quadrant', None)
    fname = kwargs.pop('fname', None)
    size = kwargs.pop('size', 50)
    title = kwargs.pop('title', None)

#     x.reset_index(inplace=True, drop=True)
#     y.reset_index(inplace=True, drop=True)

    x_min, x_max, x_avg = x.min(), x.max(), x.mean()
    y_min, y_max, y_avg = y.min(), y.max(), y.mean()

    bounds_adjuster_x = bm * max(x_max - x_avg, x_avg - x_min)
    bounds_adjuster_y = bm * max(y_max - y_avg, y_avg - y_min)
    lb_x = x_avg - bounds_adjuster_x
    ub_x = x_avg + bounds_adjuster_x
    lb_y = y_avg - bounds_adjuster_y
    ub_y = y_avg + bounds_adjuster_y

    fill_color = '#ACB9CA'
    edge_color = '#44546A'

#     fill_color = '#B4C6E7'
#     edge_color = '#4472C4'
    alpha = 1

    plt.figure(figsize=figsize)

    if highlight_quadrant:
        quadrants = pd.Series([which_quadrant(x, y, x_avg, y_avg) for x, y in zip(x, y)], index=x.index)
        quad_mask = quadrants == highlight_quadrant
        x_hl, y_hl = x[quad_mask], y[quad_mask]
        x, y = x[~quad_mask], y[~quad_mask]

        plt.scatter(x=x_hl, y=y_hl, s=size, c=fill_color, edgecolors=edge_color, linewidths=2, alpha=alpha, zorder=99)
        alpha = 0.25

    plt.plot([x_avg] * 2, [lb_y, ub_y], c='k', lw=1)
    plt.plot([lb_x, ub_x], [y_avg] * 2, c='k', lw=1)
    ax = plt.scatter(x=x, y=y, s=size, c=fill_color, edgecolors=edge_color, linewidths=2, alpha=alpha, zorder=98)

    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlim(lb_x, ub_x)
    plt.ylim(lb_y, ub_y)

    # Percentage ticks solution adapted from StackOverflow
    # https://stackoverflow.com/questions/31357611/format-y-axis-as-percent
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1, 0))
    plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(1, 0))

    if fname:
        plt.savefig(fname)


def which_quadrant(x, y, x_0, y_0):
    '''
    Helper function for make_quacrant_chart. Figures out what quadrant the data is in.
    '''
    if (x >= x_0) and (y >= y_0):
        return 1
    if (x < x_0) and (y >= y_0):
        return 2
    if (x < x_0) and (y < y_0):
        return 3
    return 4
