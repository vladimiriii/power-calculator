import numpy as np
from scipy.stats import norm, t

from app.lib import utils
from app.lib.statistics.t_test import calculate_sample_size_from_cohens_d


def generate_power_chart_data(inputs):
    sample_fields = inputs['sampleFields']
    if utils.all_sample_info_provided(sample_fields):
        d = utils.calculate_cohens_d(mu_1=float(sample_fields[0]['mean']),
                                     mu_2=float(sample_fields[1]['mean']),
                                     sigma_1=float(sample_fields[0]['stdDev']),
                                     sigma_2=float(sample_fields[1]['stdDev']))
    else:
        d = float(inputs['effectSize'])

    powers = list(np.arange(0.50, 1, 0.005))
    one_sided_sample_sizes = []
    two_sided_sample_sizes = []
    for p in powers:
        results = calculate_sample_size_from_cohens_d(d=d,
                                                      alpha=float(inputs['alpha']),
                                                      power=p,
                                                      enrolment_ratio=float(inputs['enrolmentRatio']))
        one_sided_sample_sizes.append(results[-1]['one_sided_test'])
        two_sided_sample_sizes.append(results[-1]['two_sided_test'])

    # Split into higher and lower
    test_power = float(inputs['power'])
    os_lower = [round(val, 2) if round(pow, 2) <= test_power else None for pow, val in zip(powers, one_sided_sample_sizes)]
    os_higher = [round(val, 2) if round(pow, 2) >= test_power else None for pow, val in zip(powers, one_sided_sample_sizes)]
    ts_lower = [round(val, 2) if round(pow, 2) <= test_power else None for pow, val in zip(powers, two_sided_sample_sizes)]
    ts_higher = [round(val, 2) if round(pow, 2) >= test_power else None for pow, val in zip(powers, two_sided_sample_sizes)]

    chart_data = {
        "title": "Sample Size vs Power (effect size: {:0.3f}, α: {})".format(d, inputs['alpha']),
        "xAxisLabel": "Statistical Power (1 - β)",
        "yAxisLabel": "Sample Size",
        "labels": ["{:0.3f}".format(p) for p in powers],
        "dataset": [
            {
                "label": "One Sided Test",
                "data": os_lower
            },
            {
                "label": "One Sided Test",
                "data": os_higher
            },
            {
                "label": "Two Sided Test",
                "data": ts_lower
            },
            {
                "label": "Two Sided Test",
                "data": ts_higher
            },
        ]
    }

    return chart_data


def generate_distributions_chart_data(inputs, sample_sizes):

    alpha = float(inputs['alpha'])
    n_1 = sample_sizes[0]["two_sided_test"]
    n_2 = sample_sizes[1]["two_sided_test"]
    n = n_1 + n_2 - 2

    if utils.all_sample_info_provided(inputs['sampleFields']):
        mu_1 = float(inputs['sampleFields'][0]['mean'])
        mu_2 = float(inputs['sampleFields'][1]['mean'])
        sigma_1 = float(inputs['sampleFields'][0]['stdDev'])
        sigma_2 = float(inputs['sampleFields'][1]['stdDev'])
        d = utils.calculate_cohens_d(mu_1, mu_2, sigma_1, sigma_2)
    else:
        d = float(inputs['effectSize'])
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
    x_axis_values = list(np.arange(x_min, x_max, (x_max - x_min) / 500))

    alpha_lower = t.ppf(alpha/2, df=n, loc=0, scale=se)
    alpha_upper = -1 * alpha_lower

    H0_significant = []
    H0_not_significant = []
    HA_powered = []
    HA_unpowered = []
    for value in x_axis_values:
        # Null Hypothesis
        H0_not_significant.append(t.pdf(value, df=n, loc=H0_mean, scale=se))
        if value < alpha_lower or value > alpha_upper:
            H0_significant.append(t.pdf(value, df=n, loc=H0_mean, scale=se))
        else:
            H0_significant.append(None)

        # Alternative Hypothesis
        HA_powered.append(t.pdf(value, df=n, loc=HA_mean, scale=se))
        if HA_mean < H0_mean and value > alpha_lower:
            HA_unpowered.append(t.pdf(value, df=n, loc=HA_mean, scale=se))
        elif HA_mean >= H0_mean and value < alpha_upper:
            HA_unpowered.append(t.pdf(value, df=n, loc=HA_mean, scale=se))
        else:
            HA_unpowered.append(None)

    if HA_mean < H0_mean:
        power = t.cdf(alpha_lower, df=n, loc=HA_mean, scale=se)
    else:
        power = 1 - t.cdf(alpha_upper, df=n, loc=HA_mean, scale=se)

    decimal_points = utils.determine_decimal_points(x_max)

    return {
        "title": "Distributions (effect size: {}, α: {}, power (1 - β): {:.1%})".format(round(d, utils.determine_decimal_points(d)), alpha, power),
        "xAxisLabel": "Difference in sample means",
        "yAxisLabel": "Density",
        "labels": [round(x, decimal_points) for x in x_axis_values],
        "hidePoints": True,
        "dataset": [
            {
                "label": "H0 - Significant",
                "data": H0_significant,
            },
            {
                "label": "H0",
                "data": H0_not_significant,
            },
            {
                "label": "HA - Powered",
                "data": HA_powered,
            },
            {
                "label": "HA",
                "data": HA_unpowered,
            }
        ]
    }


def generate_effect_size_chart_data(inputs):
    sample_fields = inputs['sampleFields']
    if utils.all_sample_info_provided(sample_fields):
        effect_size = utils.calculate_cohens_d(mu_1=float(sample_fields[0]['mean']),
                                               mu_2=float(sample_fields[1]['mean']),
                                               sigma_1=float(sample_fields[0]['stdDev']),
                                               sigma_2=float(sample_fields[1]['stdDev']))
    else:
        effect_size = float(inputs['effectSize'])

    step = 0.002
    window = 0.1
    window_min = effect_size - window
    window_max = effect_size + window + step
    effect_sizes = list(np.arange(window_min, window_max, step))
    # effect_sizes = [None if -0.004 < x < 0.006 else x for x in x_labels]

    one_sided_sample_sizes = []
    two_sided_sample_sizes = []
    for d in effect_sizes:
        results = calculate_sample_size_from_cohens_d(d=d,
                                                      alpha=float(inputs['alpha']),
                                                      power=float(inputs['power']),
                                                      enrolment_ratio=float(inputs['enrolmentRatio']))
        one_sided_sample_sizes.append(results[-1]['one_sided_test'])
        two_sided_sample_sizes.append(results[-1]['two_sided_test'])

    # Split into higher and lower
    max_value = 1000000
    actual_x = abs(round(effect_size, 3))
    os_lower = [round(y, 3) if -actual_x <= round(x, 3) <= actual_x and y <= max_value else None for x, y in zip(effect_sizes, one_sided_sample_sizes)]
    os_higher = [round(y, 3) if round(x, 3) <= -actual_x or round(x, 3) >= actual_x and y <= max_value else None for x, y in zip(effect_sizes, one_sided_sample_sizes)]
    ts_lower = [round(y, 3) if -actual_x <= round(x, 3) <= actual_x and y <= max_value else None for x, y in zip(effect_sizes, two_sided_sample_sizes)]
    ts_higher = [round(y, 3) if round(x, 3) <= -actual_x or round(x, 3) >= actual_x and y <= max_value else None for x, y in zip(effect_sizes, two_sided_sample_sizes)]

    chart_data = {
        "title": "Sample Size vs Effect Size (α: {}, 1 - β: {})".format(inputs['alpha'], inputs['power']),
        "xAxisLabel": "Effect Size",
        "yAxisLabel": "Sample Size",
        "labels": ["{:0.3f}".format(d) for d in effect_sizes],
        "dataset": [
            {
                "label": "Lower Powers – One Sided Test",
                "data": os_lower
            },
            {
                "label": "Higher Powers – One Sided Test",
                "data": os_higher
            },
            {
                "label": "Lower Powers – Two Sided Test",
                "data": ts_lower
            },
            {
                "label": "Higher Powers – Two Sided Test",
                "data": ts_higher
            },
        ]
    }

    return chart_data
