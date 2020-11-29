import numpy as np
import math
from scipy.stats import norm, t

from app.lib import utils, colors
from app.lib.statistics import t_test as tt


def generate_power_vs_sample_size_chart_data(d, alpha, power, enrolment_ratio):
    dps = 3
    power = round(power, dps)
    power_range = list(np.arange(0.50, 1, 0.001))
    one_sided_sample_sizes = []
    two_sided_sample_sizes = []
    for p in power_range:
        results = tt.calculate_sample_size_from_cohens_d(d=d,
                                                         alpha=alpha,
                                                         power=p,
                                                         enrolment_ratio=enrolment_ratio)
        one_sided_sample_sizes.append(results[-1][0])
        two_sided_sample_sizes.append(results[-1][1])

    # Split into higher and lower

    os_lower = [round(val, dps) if round(pow, dps) <= power else None for pow, val in zip(power_range, one_sided_sample_sizes)]
    os_higher = [round(val, dps) if round(pow, dps) >= power else None for pow, val in zip(power_range, one_sided_sample_sizes)]
    ts_lower = [round(val, dps) if round(pow, dps) <= power else None for pow, val in zip(power_range, two_sided_sample_sizes)]
    ts_higher = [round(val, dps) if round(pow, dps) >= power else None for pow, val in zip(power_range, two_sided_sample_sizes)]

    return {
        "title": "Sample Size vs Power (effect size: {:0.3f}, α: {:0.3f})".format(d, alpha),
        "xAxisLabel": "Statistical Power (1 - β)",
        "yAxisLabel": "Sample Size",
        "labels": ["{:0.3f}".format(p) for p in power_range],
        "verticalLine": {
            "position": "{:0.3f}".format(power),
            "label": "Current Power"
        },
        "dataset": [
            {
                "label": "One Sided Test",
                "data": os_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "One Sided Test",
                "data": os_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            },
            {
                "label": "Two Sided Test",
                "data": ts_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "Two Sided Test",
                "data": ts_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            }
        ]
    }


def generate_effect_size_vs_sample_size_chart_data(d, alpha, power, enrolment_ratio):
    window = 0.1
    if d < 0:
        x_max = d * (1 - window)
        x_min = d * (1 + window)
    else:
        x_min = d * (1 - window)
        x_max = d * (1 + window)
    step = (x_max - x_min) / 500
    dps = utils.determine_decimal_points(x_max)
    effect_sizes = list(np.arange(x_min, x_max, step))

    one_sided_sample_sizes = []
    two_sided_sample_sizes = []
    for es in effect_sizes:
        results = tt.calculate_sample_size_from_cohens_d(d=es,
                                                         alpha=alpha,
                                                         power=power,
                                                         enrolment_ratio=enrolment_ratio)
        one_sided_sample_sizes.append(results[-1][0])
        two_sided_sample_sizes.append(results[-1][1])

    # Split into higher and lower
    actual_x = abs(round(d, dps))
    os_lower = [round(y, dps) if -actual_x <= round(x, dps) <= actual_x else None for x, y in zip(effect_sizes, one_sided_sample_sizes)]
    os_higher = [round(y, dps) if round(x, dps) <= -actual_x or round(x, dps) >= actual_x else None for x, y in zip(effect_sizes, one_sided_sample_sizes)]
    ts_lower = [round(y, dps) if -actual_x <= round(x, dps) <= actual_x else None for x, y in zip(effect_sizes, two_sided_sample_sizes)]
    ts_higher = [round(y, dps) if round(x, dps) <= -actual_x or round(x, dps) >= actual_x else None for x, y in zip(effect_sizes, two_sided_sample_sizes)]

    format_string = "{:." + str(dps) + "f}"
    chart_data = {
        "title": "Sample Size vs Effect Size (α: {:0.3f}, power (1 - β): {:.1%})".format(alpha, power),
        "xAxisLabel": "Effect Size",
        "yAxisLabel": "Sample Size",
        "labels": [format_string.format(es) for es in effect_sizes],
        "verticalLine": {
            "position": format_string.format(d),
            "label": "Current Effect Size"
        },
        "dataset": [
            {
                "label": "Lower Powers – One Sided Test",
                "data": os_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "Higher Powers – One Sided Test",
                "data": os_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            },
            {
                "label": "Lower Powers – Two Sided Test",
                "data": ts_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "Higher Powers – Two Sided Test",
                "data": ts_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            },
        ]
    }

    return chart_data


def generate_sample_size_vs_power_chart_data(d, alpha, power, enrolment_ratio):
    n_results = tt.calculate_sample_size_from_cohens_d(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
    n_powered = tt.calculate_sample_size_from_cohens_d(d=d, alpha=alpha, power=0.8, enrolment_ratio=enrolment_ratio)
    n_target = n_results[0][1] + n_results[1][1]
    ff = 0.1
    x_min = 4
    x_max = max(n_powered[0][1] + n_powered[1][1], int(n_target * (1 + ff)))
    step = int(max(1, (x_max - x_min) / 500))
    sample_sizes = np.arange(x_min, x_max, step)
    n_target = utils.find_closest_value(sample_sizes, n_target)

    os_lower = []
    ts_lower = []
    os_upper = []
    ts_upper = []
    for n in sample_sizes:
        cn_1 = math.ceil(n * enrolment_ratio / (1 + enrolment_ratio))
        cn_2 = math.ceil(n - cn_1)
        results = tt.calculate_power_from_cohens_d(d=d, n_1=cn_1, n_2=cn_2, alpha=alpha)
        if n < n_target:
            os_lower.append(results[0][0])
            ts_lower.append(results[1][0])
            os_upper.append(None)
            ts_upper.append(None)
        elif n > n_target:
            os_lower.append(None)
            ts_lower.append(None)
            os_upper.append(results[0][0])
            ts_upper.append(results[1][0])
        elif n == n_target:
            os_lower.append(results[0][0])
            ts_lower.append(results[1][0])
            os_upper.append(results[0][0])
            ts_upper.append(results[1][0])

    # Determine X axis range
    x_axis_values = [str(x) for x in list(sample_sizes)]

    return {
        "title": "Sample Size vs Power (effect size: {:0.3f}, α: {:0.3f})".format(d, alpha),
        "xAxisLabel": "Sample Size",
        "yAxisLabel": "Statistical Power (1 - β)",
        "labels": x_axis_values,
        "verticalLine": {
            "position": str(n_target),
            "label": "Current Sample Size"
        },
        "dataset": [
            {
                "label": "One Sided Test",
                "data": os_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "One Sided Test",
                "data": os_upper,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            },
            {
                "label": "Two Sided Test",
                "data": ts_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "Two Sided Test",
                "data": ts_upper,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            }
        ]
    }


def generate_distributions_chart_data(d, alpha, n_1, n_2):
    n = n_1 + n_2 - 2
    mu_1 = 0
    mu_2 = mu_1 + d
    sigma_1 = 1
    sigma_2 = 1

    if n <= 0:
        n_1 += 1
        n_2 += 1
        n = 2
    sd_pooled = utils.calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)
    H0_mean = 0
    HA_mean = mu_2 - mu_1
    se = sd_pooled * (1/n_1 + 1/n_2)**0.5

    # Determine X axis range
    x_min = min(H0_mean, HA_mean) - (se * 5)
    x_max = max(H0_mean, HA_mean) + (se * 5)
    x_axis_values = list(np.arange(x_min, x_max, (x_max - x_min) / 1000))

    alpha_lower = norm.ppf(alpha/2, loc=0, scale=se)
    alpha_upper = -1 * alpha_lower

    H0_significant = []
    H0_not_significant = []
    HA_powered = []
    HA_unpowered = []
    threshold = alpha_upper if HA_mean >= H0_mean else alpha_lower
    for value in x_axis_values:
        # Null Hypothesis
        H0_not_significant.append(norm.pdf(value, loc=H0_mean, scale=se))
        if value < alpha_lower or value > alpha_upper:
            H0_significant.append(norm.pdf(value, loc=H0_mean, scale=se))
        else:
            H0_significant.append(None)

        # Alternative Hypothesis
        HA_powered.append(norm.pdf(value, loc=HA_mean, scale=se))
        if HA_mean < H0_mean and value > alpha_lower:
            HA_unpowered.append(norm.pdf(value, loc=HA_mean, scale=se))
        elif HA_mean >= H0_mean and value < alpha_upper:
            HA_unpowered.append(norm.pdf(value, loc=HA_mean, scale=se))
        else:
            HA_unpowered.append(None)

    if HA_mean < H0_mean:
        power = norm.cdf(alpha_lower, loc=HA_mean, scale=se)
        threshold = alpha_lower
    else:
        power = 1 - norm.cdf(alpha_upper, loc=HA_mean, scale=se)
        threshold = alpha_upper

    decimal_points = utils.determine_decimal_points(x_max)
    format_string = "{:." + str(decimal_points) + "f}"

    return {
        "title": "Distributions (effect size: {:0.3f}, α: {:0.3f}, power (1 - β): {:.1%})".format(d, alpha, power),
        "xAxisLabel": "Difference in population means",
        "yAxisLabel": "Density",
        "labels": [format_string.format(x) for x in x_axis_values],
        "verticalLine": {
            "position": format_string.format(utils.find_closest_value(x_axis_values, threshold)),
            "label": "Threshold"
        },
        "hidePoints": True,
        "dataset": [
            {
                "label": "H0 - Significant",
                "data": H0_significant,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "H0",
                "data": H0_not_significant,
                "borderColor": colors.line_colors[0],
                "backgroundColor": None
            },
            {
                "label": "HA - Powered",
                "data": HA_powered,
                "borderColor": colors.line_colors[1],
                "backgroundColor": None
            },
            {
                "label": "HA",
                "data": HA_unpowered,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            }
        ]
    }


def generate_t_distribution_chart_data(alpha, t_stat, n_1, n_2, x_bar_1, x_bar_2, s_1, s_2):
    welches_df = utils.welches_degrees_of_freedom(s_1, n_1, s_2, n_2)
    d = utils.calculate_cohens_d(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2)
    alpha_upper = t.ppf(1 - alpha/2, df=welches_df)
    alpha_lower = -alpha_upper

    # Determine X axis range
    x_min = -5
    x_max = 5
    x_axis = list(np.arange(x_min, x_max, (x_max - x_min) / 501))
    x_axis_values = ["{:.3f}".format(x) for x in x_axis]

    H0 = []
    significant = []
    for value in x_axis:
        H0.append(t.pdf(value, df=welches_df))
        if alpha_lower <= value <= alpha_upper:
            significant.append(None)
        else:
            significant.append(t.pdf(value, df=welches_df))


    return {
        "title": "Null Hypothesis t-distribution (effect size: {:.3f})".format(d),
        "xAxisLabel": "t",
        "yAxisLabel": "Density",
        "labels": x_axis_values,
        "verticalLine": {
            "position": "{:.3f}".format(utils.find_closest_value(x_axis, t_stat)),
            "label": "t statistic"
        },
        "dataset": [
            {
                "label": "H0",
                "data": H0,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": None
            },
            {
                "label": "H0",
                "data": significant,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            }
        ]
    }


def generate_t_statistic_vs_sample_size_chart_data(n_1, n_2, x_bar_1, x_bar_2, s_1, s_2, alpha):
    d_actual = utils.calculate_cohens_d(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2)
    n_actual = n_1 + n_2
    r_e = n_1/n_2
    n_results = tt.calculate_sample_size_from_means(mu_1=x_bar_1, mu_2=x_bar_2, sigma_1=s_1, sigma_2=s_2, alpha=alpha, power=0.5, enrolment_ratio=r_e)
    n_target = n_results[0][1] + n_results[1][1]
    ff = 0.1
    x_min = int(max(4, min(n_actual * (1 - ff), n_target * (1 - ff))))
    x_max = int(max(n_actual * (1 + ff), n_target * (1 + ff)))
    step = int(max(1, (x_max - x_min) / 500))
    sample_sizes = np.arange(x_min, x_max, step)
    n_actual = utils.find_closest_value(sample_sizes, n_actual)
    n_target = utils.find_closest_value(sample_sizes, n_target)

    t_stat_lower = []
    t_stat_higher = []
    for n in sample_sizes:
        cn_1 = math.ceil(n * r_e / (1 + r_e))
        cn_2 = math.ceil(n - cn_1)
        welches_df = utils.welches_degrees_of_freedom(s_1, cn_1, s_2, cn_2)
        d = utils.calculate_cohens_d(x_bar_1, s_1, cn_1, x_bar_2, s_2, cn_2)
        t_stat = tt.calculate_t_stat_from_cohens_d(d, cn_1, cn_2)
        if n <= n_target:
            t_stat_lower.append(t_stat)
        else:
            t_stat_lower.append(None)
        if n >= n_target:
            t_stat_higher.append(t_stat)
        else:
            t_stat_higher.append(None)

    # Determine X axis range
    x_axis_values = [str(x) for x in list(sample_sizes)]

    return {
        "title": "t-statistic vs Sample Size (effect size: {:.3f}, enrolment ratio: {:.3f})".format(d_actual, n_1/n_2),
        "xAxisLabel": "Total Samples",
        "yAxisLabel": "t-statistic",
        "labels": x_axis_values,
        "verticalLine": {
            "position": str(n_actual),
            "label": "Current Sample Size"
        },
        "dataset": [
            {
                "label": "t-statistic",
                "data": t_stat_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "t-statistic",
                "data": t_stat_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            }
        ]
    }


def generate_t_statistic_vs_effect_size_chart_data(n_1, n_2, x_bar_1, x_bar_2, s_1, s_2, alpha):
    d_actual = utils.calculate_cohens_d(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2)
    d_results = tt.calculate_min_effect_size(n_1=n_1, n_2=n_2, alpha=alpha, power=0.5)
    d_target = d_results[1][0]
    ff = 0.5
    if d_actual < 0:
        x_min = min(-d_target, d_actual) * (1 + ff)
        x_max = max(-d_target, d_actual) * (1 - ff)
    else:
        x_min = min(d_target, d_actual) * (1 - ff)
        x_max = max(d_target, d_actual) * (1 + ff)

    # Rounding to ensure matches
    step = (x_max - x_min) / 500
    dps = utils.determine_decimal_points(x_max)
    effect_sizes = [round(x, dps) for x in np.arange(x_min, x_max, step)]
    d_actual = utils.find_closest_value(effect_sizes, d_actual)
    d_target = utils.find_closest_value(effect_sizes, d_target)

    t_stat_lower = []
    t_stat_higher = []
    for d in effect_sizes:
        t_stat = tt.calculate_t_stat_from_cohens_d(d, n_1, n_2)
        if d <= d_target:
            t_stat_lower.append(t_stat)
        else:
            t_stat_lower.append(None)
        if d >= d_target:
            t_stat_higher.append(t_stat)
        else:
            t_stat_higher.append(None)

    # Determine X axis range
    format_string = "{:." + str(dps) + "f}"
    x_axis_values = [format_string.format(x) for x in list(effect_sizes)]

    return {
        "title": "t-statistic vs Effect Size (sample size: {}, enrolment ratio: {:.3f})".format(n_1 + n_2, n_1/n_2),
        "xAxisLabel": "Effect Size",
        "yAxisLabel": "t-statistic",
        "labels": x_axis_values,
        "verticalLine": {
            "position": format_string.format(d_actual),
            "label": "Current Effect Size"
        },
        "dataset": [
            {
                "label": "t-statistic",
                "data": t_stat_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "t-statistic",
                "data": t_stat_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            }
        ]
    }


def generate_p_value_vs_sample_size_chart_data(n_1, n_2, x_bar_1, x_bar_2, s_1, s_2, alpha):
    d_actual = utils.calculate_cohens_d(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2)
    n_actual = n_1 + n_2
    r_e = n_1 / n_2
    n_results = tt.calculate_sample_size_from_means(mu_1=x_bar_1, mu_2=x_bar_2, sigma_1=s_1, sigma_2=s_2, alpha=alpha, power=0.5, enrolment_ratio=r_e)
    n_target = n_results[0][1] + n_results[1][1]
    ff = 0.1
    x_min = int(max(4, min(n_actual * (1 - ff), n_target * (1 - ff))))
    x_max = int(max(n_actual * (1 + ff), n_target * (1 + ff)))
    step = int(max(1, (x_max - x_min) / 500))
    sample_sizes = np.arange(x_min, x_max, step)
    n_actual = utils.find_closest_value(sample_sizes, n_actual)
    n_target = utils.find_closest_value(sample_sizes, n_target)

    os_lower = []
    ts_lower = []
    os_higher = []
    ts_higher = []
    for n in sample_sizes:
        cn_1 = math.ceil(n * r_e / (1 + r_e))
        cn_2 = math.ceil(n - cn_1)
        welches_df = utils.welches_degrees_of_freedom(s_1, cn_1, s_2, cn_2)
        d = utils.calculate_cohens_d(x_bar_1, s_1, cn_1, x_bar_2, s_2, cn_2)
        t_stat = tt.calculate_t_stat_from_cohens_d(d, cn_1, cn_2)
        results = tt.calculate_p_value(t_stat, welches_df)
        if n <= n_target:
            os_lower.append(results[0][0])
            ts_lower.append(results[1][0])
        else:
            os_lower.append(None)
            ts_lower.append(None)
        if n >= n_target:
            os_higher.append(results[0][0])
            ts_higher.append(results[1][0])
        else:
            os_higher.append(None)
            ts_higher.append(None)

    # Determine X axis range
    x_axis_values = [str(x) for x in list(sample_sizes)]

    return {
        "title": "Sample Size vs p-value (effect size: {:.3f}, enrolment ratio: {:.3f})".format(d_actual, n_1/n_2),
        "xAxisLabel": "Total Samples",
        "yAxisLabel": "p-value",
        "labels": x_axis_values,
        "verticalLine": {
            "position": str(n_actual),
            "label": "Current Sample Size"
        },
        "dataset": [
            {
                "label": "One Sided Test",
                "data": os_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "One Sided Test",
                "data": os_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            },
            {
                "label": "Two Sided Test",
                "data": ts_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "Two Sided Test",
                "data": ts_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            }
        ]
    }


def generate_p_value_vs_effect_size_chart_data(n_1, n_2, x_bar_1, x_bar_2, s_1, s_2, alpha):
    d_actual = utils.calculate_cohens_d(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2)
    d_results = tt.calculate_min_effect_size(n_1=n_1, n_2=n_2, alpha=alpha, power=0.5)
    d_target = d_results[1][0]
    ff = 0.5
    if d_actual < 0:
        x_min = min(-d_target, d_actual) * (1 + ff)
        x_max = max(-d_target, d_actual) * (1 - ff)
    else:
        x_min = min(d_target, d_actual) * (1 - ff)
        x_max = max(d_target, d_actual) * (1 + ff)

    # Rounding to ensure matches
    step = (x_max - x_min) / 500
    dps = utils.determine_decimal_points(x_max)
    effect_sizes = [round(x, dps) for x in np.arange(x_min, x_max, step)]
    d_actual = utils.find_closest_value(effect_sizes, d_actual)
    d_target = utils.find_closest_value(effect_sizes, d_target)

    os_lower = []
    ts_lower = []
    os_higher = []
    ts_higher = []
    for d in effect_sizes:
        welches_df = utils.welches_degrees_of_freedom(s_1, n_1, s_2, n_2)
        t_stat = tt.calculate_t_stat_from_cohens_d(d, n_1, n_2)
        results = tt.calculate_p_value(t_stat, welches_df)
        if d <= d_target:
            os_lower.append(results[0][0])
            ts_lower.append(results[1][0])
        else:
            os_lower.append(None)
            ts_lower.append(None)
        if d >= d_target:
            os_higher.append(results[0][0])
            ts_higher.append(results[1][0])
        else:
            os_higher.append(None)
            ts_higher.append(None)

    # Determine X axis range
    format_string = "{:." + str(dps) + "f}"
    x_axis_values = [format_string.format(x) for x in list(effect_sizes)]

    return {
        "title": "p-value vs Effect Size (sample size: {}, enrolment ratio: {:.3f})".format(n_1 + n_2, n_1/n_2),
        "xAxisLabel": "Effect Size",
        "yAxisLabel": "p-value",
        "labels": x_axis_values,
        "verticalLine": {
            "position": format_string.format(d_actual),
            "label": "Current Effect Size"
        },
        "dataset": [
            {
                "label": "One Sided Test",
                "data": os_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "One Sided Test",
                "data": os_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            },
            {
                "label": "Two Sided Test",
                "data": ts_lower,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[0],
                "backgroundColor": colors.background_colors[0]
            },
            {
                "label": "Two Sided Test",
                "data": ts_higher,
                "pointBorderWidth": 0,
                "pointRadius": 0.5,
                "borderColor": colors.line_colors[1],
                "backgroundColor": colors.background_colors[1]
            }
        ]
    }
