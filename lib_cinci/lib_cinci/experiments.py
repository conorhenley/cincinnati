from collections import defaultdict
import matplotlib.pyplot as plt


def group_experiments_by(data, fn):
    res = defaultdict(list)
    for element in data:
        key = fn(element)
        res[key].append(element)
    return res


def models_plot(models, plotting_fn, grouping_fn=None):
    '''
        This functions takes a list with models (as obtained from MongoDB)
        along with a grouping function and a plotting one.

        First, models are grouped depending on grouping_fn result applied to
        each model. Then the plotting_fn is applied and is expected to return
        arguments to matplotlibs plot function.

        Groups are plotted on different axes

        experiment_name in model is used as legend.

        If grouping_fn is None, all plots are done in the same axes.


    '''
    # If grouping functions is none, replace it with a dummy function
    grouping_fn = (lambda model: 1) if grouping_fn is None else grouping_fn

    # Group experiments using grouping fn
    groups = group_experiments_by(models, fn=grouping_fn)

    # Print group key and len
    # for k, models_group in groups.iteritems():
    #    print '{} with {} elements'.format(k, len(models_group))

    # Get number of groups and matplolib axes object
    n_groups = len(groups.keys())
    fig, axes = plt.subplots(nrows=n_groups,
                             ncols=1, figsize=(20, 5 * n_groups))
    axes = [axes] if n_groups == 1 else axes

    # Plot
    # Iterate over every group
    for ax, (key, model_group) in zip(axes, groups.iteritems()):
        # Iterate over every model for every group
        for m in model_group:
            ax.plot(*plotting_fn(m))
        ax.legend([m['experiment_name'] for m in model_group])
