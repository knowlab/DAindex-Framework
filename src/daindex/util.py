import matplotlib.pyplot as plt
import numpy as np

from daindex.core import db_ineq, deterioration_index


# get the random sample for obtaining deterioration index
def get_random_sample(df, feature, feature_gen_fun=None):
    if feature_gen_fun is not None:
        X = df.apply(feature_gen_fun, axis=1).to_numpy().reshape(-1, 1)
    else:
        X = df[feature].to_numpy().reshape(-1, 1)
    return X


def compare_two_groups(
    df1,
    df2,
    feature,
    cohort_name1,
    cohort_name2,
    di_label,
    threshold,
    bandwidth=1,
    is_discrete=False,
    search_bandwidth=True,
    do_plot=True,
    feature_gen_fun=None,
    reverse=False,
):
    """
    # obtain the inequality quantification
    df1 - data frame of the first group
    df2 - data frame of the second group
    feature - the feature name of the measurement, not used if feature_gen_fun is not none
    cohort_name1 - the name of the first cohort to be displayed on the plot
    cohort_name2 - the name of the second cohort to be displayed on the plot
    di_label - the label of the deterioration index to be displayed on the plot
    threshold - the threshold for abnormality starting point. This could be a list
        if two cohorts require different thresholds. For example, male/female might have
        different normal ranges for some measurements. The first element will be used for the first one.
    """
    X1 = get_random_sample(df1, feature, feature_gen_fun=feature_gen_fun)
    X2 = get_random_sample(df2, feature, feature_gen_fun=feature_gen_fun)
    # it is very important to use the same min/max values as the k-step weighting needs to
    # put the same weight for the same level of deterioration
    min_v = min([np.min(X1), np.min(X2)])
    max_v = max([np.max(X1), np.max(X2)])

    threshold1 = threshold
    threshold2 = threshold
    if type(threshold) is list:
        threshold1 = threshold[0]
        threshold2 = threshold[1]
    c1_di = deterioration_index(
        X1,
        min_v,
        max_v,
        reverse=reverse,
        threshold=threshold1,
        bandwidth=bandwidth,
        is_discrete=is_discrete,
        plot_title=f"{cohort_name1}| {di_label}",
        search_bandwidth=search_bandwidth,
        do_plot=do_plot,
    )
    c2_di = deterioration_index(
        X2,
        min_v,
        max_v,
        reverse=reverse,
        threshold=threshold2,
        bandwidth=bandwidth,
        is_discrete=is_discrete,
        plot_title=f"{cohort_name2}| {di_label}",
        search_bandwidth=search_bandwidth,
        do_plot=do_plot,
    )
    ineq = db_ineq(c1_di, c2_di)
    # print(f'{cohort_name1} vs {cohort_name2} inequality on {di_label} is {ineq:.2%}')
    return c1_di, c2_di, ineq


def area(w_data):
    """
    calculate the area under curve - do NOT do interpolation
    """
    prev = None
    area = 0
    decision_area = 0
    n_points = 0
    for r in w_data:
        if prev is not None:
            a = (r[1] + prev[1]) * (r[0] - prev[0]) / 2  # * r[2]
            area += a
            if prev[0] >= 0.5:
                decision_area += a
                n_points += 1
        prev = r

    if prev is not None:
        a = (r[1] + prev[1]) * (r[0] - prev[0]) / 2  # * r[2]
        area += a
        if prev[0] >= 0.5:
            decision_area += a
            n_points += 1

    return area, decision_area


def vis_DA_indices(data, label):
    """
    plot dot-line for approximating a DA curve
    """
    w_data = data[np.where(data[:, 1] > 0)][:, [0, 2, 1]]
    a, decision_area = area(w_data)
    plt.plot(w_data[:, 0], w_data[:, 1], "-")
    plt.plot(w_data[:, 0], w_data[:, 1], "o", label=label)
    return a, decision_area, w_data


def viz(d1, d2, g1_label, g2_label, deterioration_label, allocation_label, config):
    """
    do DA curve visualisation
    """
    if "style" in config:
        plt.style.use(config["style"])
    font_size = config["font_size"] if "font_size" in config else 12
    if "fig_size" in config:
        fig = plt.figure(figsize=config["fig_size"], dpi=200)

    # do some clearning: remove those empty points
    d1 = np.delete(d1, np.where(d1[:, 1] == 0), axis=0)
    d2 = np.delete(d2, np.where(d2[:, 1] == 0), axis=0)
    # make two datasets even in terms of max x val
    x_min = min(np.max(d1[:, 0]), np.max(d2[:, 0]))
    d1 = np.delete(d1, np.where(d1[:, 0] > x_min), axis=0)
    d2 = np.delete(d2, np.where(d2[:, 0] > x_min), axis=0)

    # automatically set x/y limits for better viz
    # x_max = max(np.max(d1[:, 0]), np.max(d2[:, 0]))
    y_max = max(np.max(d1[:, 2]), np.max(d2[:, 2]))

    plt.xlim(0, x_min * 1.05)
    plt.ylim(0, y_max * 1.05)

    # do plots
    a1, da1, _ = vis_DA_indices(d1, g1_label)
    a2, da2, _ = vis_DA_indices(d2, g2_label)

    # generate output
    # print('{0}\t{1:.2%}\t{2:.2%}\t{3:.2%}'.format(deterioration, white_d_ratio, non_white_d_ratio,
    #                                      (non_white_d_ratio - white_d_ratio)/white_d_ratio))
    print("AUC\t{0:.6f}\t{1:.6f}\t{2:.2%}".format(a1, a2, (a2 - a1) / a1))
    print("Decision AUC\t{0:.6f}\t{1:.6f}\t{2:.2%}".format(da1, da2, (da2 - da1) / da1))

    # figure finishing up
    plt.xlabel(allocation_label, fontsize=font_size)
    plt.ylabel(deterioration_label, fontsize=font_size)

    # plot decision region
    plt.plot([0.5, 0.5], [0, 1], "--", lw=0.8, color="g")
    plt.axvspan(0.5, 1, facecolor="b", alpha=0.1)

    plt.legend(fontsize=font_size, loc="best")