# -*- coding: utf-8 -*-
from scipy.stats import norm, t, ttest_ind, ttest_ind_from_stats
import math
import pandas as pd
from app.lib import utils


def calculate_sample_size_from_cohens_d(d, alpha, power, q_1=0.5):
    q_2 = 1 - q_1
    p = (1/q_1 + 1/q_2)
    d_squared = d**2

    # Calculate with Normal distribution
    z_a_one_sided = norm.ppf(1 - alpha)
    z_a_two_sided = norm.ppf(1 - alpha/2)
    z_b_one_sided = norm.ppf(power)

    z_total_os = (z_a_one_sided + z_b_one_sided)**2
    z_total_ts = (z_a_two_sided + z_b_one_sided)**2

    n_one_sided = math.ceil(p * z_total_os / d_squared)
    n_two_sided = math.ceil(p * z_total_ts / d_squared)

    # Round and convert to even number
    if n_one_sided % 2 == 1:
        n_one_sided = n_one_sided + 1
    if n_two_sided % 2 == 1:
        n_two_sided = n_two_sided + 1

    results = {
        "one_sided_test": {"total_samples": n_one_sided, "group_1": math.ceil(n_one_sided * q_1), "group_2": math.ceil(n_one_sided * (1 - q_1))},
        "two_sided_test": {"total_samples": n_two_sided, "group_1": math.ceil(n_two_sided * q_1), "group_2": math.ceil(n_two_sided * (1 - q_1))}
    }

    return pd.DataFrame(results)


def calculate_sample_size_from_means(mu_1, mu_2, sigma_1, sigma_2, alpha, power, q_1=0.5):
    q_2 = 1 - q_1
    combined_sigma = (sigma_1**2 + sigma_2**2)
    mu_diff = (mu_1 - mu_2)**2

    # Calculate with Normal distribution
    z_a_one_sided = norm.ppf(1 - alpha)
    z_a_two_sided = norm.ppf(1 - alpha/2)
    z_b_one_sided = norm.ppf(power)

    z_total_os = (z_a_one_sided + z_b_one_sided)**2
    z_total_ts = (z_a_two_sided + z_b_one_sided)**2

    n_one_sided = math.ceil(2 * combined_sigma * z_total_os / mu_diff)
    n_two_sided = math.ceil(2 * combined_sigma * z_total_ts / mu_diff)

    # Round and convert to even number
    if n_one_sided % 2 == 1:
        n_one_sided = n_one_sided + 1
    if n_two_sided % 2 == 1:
        n_two_sided = n_two_sided + 1

    results = {
        "one_sided_test": {"total_samples": n_one_sided, "group_1": math.ceil(n_one_sided * q_1), "group_2": math.ceil(n_one_sided * (1 - q_1))},
        "two_sided_test": {"total_samples": n_two_sided, "group_1": math.ceil(n_two_sided * q_1), "group_2": math.ceil(n_two_sided * (1 - q_1))}
    }

    return pd.DataFrame(results)


def independent_two_sample_test_stats(n_1, n_2, mu_1, mu_2, sigma_1, sigma_2):
    n_root = (1/n_1 + 1/n_2)**0.5
    sd_pooled = utils.calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)
    standard_error = sd_pooled * n_root
    diff = abs(mu_1 - mu_2)

    t_stat = diff/standard_error
    one_sided_p = 1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat)
    two_sided_p = 2 * (1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat))

    return {"t-stat": t_stat, "p-value (one-sided)": one_sided_p, "p-value (two-sided)": two_sided_p}


def independent_two_sample_test_effect_size(n_1, n_2, d):
    n_root = (1/n_1 + 1/n_2)**0.5
    t_stat = d/n_root

    one_sided_p = 1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat)
    two_sided_p = 2 * (1 - t.cdf(df=(n_1 + n_2 - 2), x=t_stat))

    return {"t-stat": t_stat, "p-value (one-sided)": one_sided_p, "p-value (two-sided)": two_sided_p}
