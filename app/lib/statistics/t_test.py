# -*- coding: utf-8 -*-
from scipy.stats import norm, t, ttest_ind, ttest_ind_from_stats
import math
import pandas as pd
from app.lib import utils


def calculate_statistics(inputs):
    sample_fields = inputs['sampleFields']
    if inputs['target'] == "sample-size":
        if utils.all_sample_info_provided(sample_fields):
            results = calculate_sample_size_from_means(mu_1=float(sample_fields[0]['mean']),
                                                       mu_2=float(sample_fields[1]['mean']),
                                                       sigma_1=float(sample_fields[0]['stdDev']),
                                                       sigma_2=float(sample_fields[1]['stdDev']),
                                                       alpha=float(inputs['alpha']),
                                                       power=float(inputs['power']),
                                                       enrolment_ratio=float(inputs['enrolmentRatio']))
        else:
            results = calculate_sample_size_from_cohens_d(d=float(inputs['effectSize']),
                                                          alpha=float(inputs['alpha']),
                                                          power=float(inputs['power']),
                                                          enrolment_ratio=float(inputs['enrolmentRatio']))
    elif inputs['target'] == "power":
        if utils.all_sample_info_provided(sample_fields):
            results = calculate_power_from_means(mu_1=float(sample_fields[0]['mean']),
                                                 sigma_1=float(sample_fields[0]['stdDev']),
                                                 n_1=float(sample_fields[0]['n']),
                                                 mu_2=float(sample_fields[1]['mean']),
                                                 sigma_2=float(sample_fields[1]['stdDev']),
                                                 n_2=float(sample_fields[1]['n']),
                                                 alpha=float(inputs['alpha']))
        else:
            results = calculate_power_from_cohens_d(d=float(inputs['effectSize']),
                                                    n_1=float(sample_fields[0]['n']),
                                                    n_2=float(sample_fields[1]['n']),
                                                    alpha=float(inputs['alpha']))

    elif inputs['target'] == "p-value":
        if utils.all_sample_info_provided(sample_fields):
            results = caclulate_p_value_from_means(mu_1=float(sample_fields[0]['mean']),
                                                   sigma_1=float(sample_fields[0]['stdDev']),
                                                   n_1=float(sample_fields[0]['n']),
                                                   mu_2=float(sample_fields[1]['mean']),
                                                   sigma_2=float(sample_fields[1]['stdDev']),
                                                   n_2=float(sample_fields[1]['n']))
        else:
            results = caclulate_p_value_from_cohens_d(d=float(inputs['effectSize']),
                                                      n_1=float(sample_fields[0]['n']),
                                                      n_2=float(sample_fields[1]['n']))
    elif inputs['target'] == "min-effect":
        if utils.all_sample_info_provided(sample_fields):
            results = caclulate_min_effect_size(n_1=float(sample_fields[0]['n']),
                                                n_2=float(sample_fields[1]['n']),
                                                alpha=float(inputs['alpha']),
                                                power=float(inputs['power']))

    return results


def calculate_sample_size_from_cohens_d(d, alpha, power, enrolment_ratio):
    d_squared = d**2 if d != 0 else 0.00000000001
    power = power if power < 1 else 0.99999999999
    alpha = alpha if alpha != 0 else 0.0000000001

    # Calculate with Normal distribution because we don't know the df for a t distribution
    z_a_one_sided = norm.ppf(1 - alpha)
    z_a_two_sided = norm.ppf(1 - alpha/2)
    z_b_one_sided = norm.ppf(power)

    z_total_os = (z_a_one_sided + z_b_one_sided)**2
    z_total_ts = (z_a_two_sided + z_b_one_sided)**2

    n_1_os = math.ceil((1 + enrolment_ratio) * z_total_os / d_squared)
    n_1_ts = math.ceil((1 + enrolment_ratio) * z_total_ts / d_squared)

    return [
        {
            "label": "Group 1",
            "one_sided_test": n_1_os,
            "two_sided_test": n_1_ts
        },
        {
            "label": "Group 2",
            "one_sided_test": math.ceil(n_1_os / enrolment_ratio),
            "two_sided_test": math.ceil(n_1_ts / enrolment_ratio)
        },
        {
            "label": "All Samples",
            "one_sided_test": n_1_os + math.ceil(n_1_os / enrolment_ratio),
            "two_sided_test": n_1_ts + math.ceil(n_1_ts / enrolment_ratio)
        }
    ]


def calculate_sample_size_from_means(mu_1, mu_2, sigma_1, sigma_2, alpha, power, enrolment_ratio):
    combined_sigma = (sigma_1**2 + enrolment_ratio * sigma_2**2)
    mu_diff = (mu_1 - mu_2)**2

    # Calculate with Normal distribution
    z_a_one_sided = norm.ppf(1 - alpha)
    z_a_two_sided = norm.ppf(1 - alpha/2)
    z_b_one_sided = norm.ppf(power)

    z_total_os = (z_a_one_sided + z_b_one_sided)**2
    z_total_ts = (z_a_two_sided + z_b_one_sided)**2

    n_1_os = math.ceil(combined_sigma * z_total_os / mu_diff)
    n_1_ts = math.ceil(combined_sigma * z_total_ts / mu_diff)

    return [
        {
            "label": "Group 1",
            "one_sided_test": n_1_os,
            "two_sided_test": n_1_ts
        },
        {
            "label": "Group 2",
            "one_sided_test": math.ceil(n_1_os / enrolment_ratio),
            "two_sided_test": math.ceil(n_1_ts / enrolment_ratio)
        },
        {
            "label": "All Samples",
            "one_sided_test": n_1_os + math.ceil(n_1_os / enrolment_ratio),
            "two_sided_test": n_1_ts + math.ceil(n_1_ts / enrolment_ratio)
        }
    ]


def calculate_power_from_cohens_d(d, n_1, n_2, alpha):
    denominator = (1 / n_1 + 1 / n_2)**0.5
    Z_os = t.ppf(1 - alpha, df=n_1 + n_2)
    Z_ts = t.ppf(1 - alpha/2, df=n_1 + n_2)
    power_os = t.cdf(-Z_os + abs(d)/denominator, n_1 + n_2)
    power_ts = t.cdf(-Z_ts + abs(d)/denominator, n_1 + n_2)

    return [{
        "label": "Statistical Power (1 - β)",
        "one_sided_test": power_os,
        "two_sided_test": power_ts
    }]


def calculate_power_from_means(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2, alpha):
    diff = abs(mu_1 - mu_2)
    denominator = (sigma_1**2 / n_1 + sigma_2**2 / n_2)**0.5
    Z_os = t.ppf(1 - alpha, df=n_1 + n_2)
    Z_ts = t.ppf(1 - alpha/2, df=n_1 + n_2)
    power_os = t.cdf(-Z_os + diff/denominator, n_1 + n_2)
    power_ts = t.cdf(-Z_ts + diff/denominator, n_1 + n_2)

    return [{
        "label": "Statistical Power (1 - β)",
        "one_sided_test": power_os,
        "two_sided_test": power_ts
    }]


def caclulate_p_value_from_cohens_d(d, n_1, n_2):
    n_root = (1/n_1 + 1/n_2)**0.5
    t_stat = d/n_root

    one_sided_p = 1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat)
    two_sided_p = 2 * (1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat))

    return [{
        "label": "p value",
        "one_sided_test": one_sided_p,
        "two_sided_test": two_sided_p
    }]


def caclulate_p_value_from_means(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2):
    n_root = (1/n_1 + 1/n_2)**0.5
    sd_pooled = utils.calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)
    standard_error = sd_pooled * n_root
    diff = abs(mu_1 - mu_2)

    t_stat = diff/standard_error
    one_sided_p = 1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat)
    two_sided_p = 2 * (1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat))

    return [{
        "label": "p value",
        "one_sided_test": one_sided_p,
        "two_sided_test": two_sided_p
    }]


def caclulate_min_effect_size(n_1, n_2, alpha, power):
    power = power if power < 1 else 0.99999999999
    alpha = alpha if alpha != 0 else 0.0000000001
    enrolment_ratio = n_1 / n_2

    # Calculate with Normal distribution
    z_a_one_sided = t.ppf(1 - alpha, df=n_1 + n_2)
    z_a_two_sided = t.ppf(1 - alpha/2, df=n_1 + n_2)
    z_b_one_sided = t.ppf(power, df=n_1 + n_2)

    z_total_os = (z_a_one_sided + z_b_one_sided)**2
    z_total_ts = (z_a_two_sided + z_b_one_sided)**2

    d_os = ((1 + enrolment_ratio) * z_total_os / n_1)**0.5
    d_ts = ((1 + enrolment_ratio) * z_total_ts / n_1)**0.5

    return [{
        "label": "Minimum effect size",
        "one_sided_test": d_os,
        "two_sided_test": d_ts
    }]
