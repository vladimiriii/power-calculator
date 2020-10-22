import numpy as np
from app.lib import utils
from app.lib.statistics.t_test import calculate_sample_size_from_cohens_d


def generate_power_chart_data(inputs):
    sample_fields = inputs['sampleFields']
    if utils.all_sample_info_provided(sample_fields):
        d = utils.calculate_cohens_d(n_1=float(sample_fields[0]['mean']),
                                     n_2=float(sample_fields[1]['mean']),
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
        "title": "Sample Size vs Power (effect size: {:0.2f}, α: {})".format(d, inputs['alpha']),
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


def generate_effect_size_chart_data(inputs):
    sample_fields = inputs['sampleFields']
    if utils.all_sample_info_provided(sample_fields):
        effect_size = utils.calculate_cohens_d(n_1=float(sample_fields[0]['mean']),
                                               n_2=float(sample_fields[1]['mean']),
                                               sigma_1=float(sample_fields[0]['stdDev']),
                                               sigma_2=float(sample_fields[1]['stdDev']))
    else:
        effect_size = float(inputs['effectSize'])

    effect_sizes = list(np.arange(max(0.002, effect_size - 0.1), effect_size + 0.102, 0.002))
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
    os_lower = [round(val, 3) if round(es, 3) <= effect_size else None for es, val in zip(effect_sizes, one_sided_sample_sizes)]
    os_higher = [round(val, 3) if round(es, 3) >= effect_size else None for es, val in zip(effect_sizes, one_sided_sample_sizes)]
    ts_lower = [round(val, 3) if round(es, 3) <= effect_size else None for es, val in zip(effect_sizes, two_sided_sample_sizes)]
    ts_higher = [round(val, 3) if round(es, 3) >= effect_size else None for es, val in zip(effect_sizes, two_sided_sample_sizes)]

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
