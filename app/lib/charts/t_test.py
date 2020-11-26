import numpy as np
from scipy.stats import norm, t

from app.lib import utils, colors
from app.lib.statistics.t_test import calculate_sample_size_from_cohens_d


def generate_power_chart_data(d, alpha, power, enrolment_ratio):
    dps = 3
    power = round(power, dps)
    power_range = list(np.arange(0.50, 1, 0.001))
    one_sided_sample_sizes = []
    two_sided_sample_sizes = []
    for p in power_range:
        results = calculate_sample_size_from_cohens_d(d=d,
                                                      alpha=alpha,
                                                      power=p,
                                                      enrolment_ratio=enrolment_ratio)
        one_sided_sample_sizes.append(results[-1]['one_sided_test'])
        two_sided_sample_sizes.append(results[-1]['two_sided_test'])

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


def generate_effect_size_chart_data(d, alpha, power, enrolment_ratio):
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
        results = calculate_sample_size_from_cohens_d(d=es,
                                                      alpha=alpha,
                                                      power=power,
                                                      enrolment_ratio=enrolment_ratio)
        one_sided_sample_sizes.append(results[-1]['one_sided_test'])
        two_sided_sample_sizes.append(results[-1]['two_sided_test'])

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


def generate_t_distribution_chart_data(t_stat, n_1, n_2, s_1, s_2):
    welches_df = utils.welches_degrees_of_freedom(s_1, n_1, s_2, n_2)

    # Determine X axis range
    x_min = -5
    x_max = 5
    x_axis = list(np.arange(x_min, x_max, (x_max - x_min) / 500))
    x_axis_values = ["{:.3f}".format(x) for x in x_axis]

    H0 = []
    for value in x_axis:
        H0.append(t.pdf(value, loc=0, df=welches_df))

    return {
        "title": "Null Hypothesis t-distribution",
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
            }
        ]
    }
