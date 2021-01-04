# -*- coding: utf-8 -*-
from scipy.stats import norm, t, ttest_ind, ttest_ind_from_stats
import math
import pandas as pd
from app.lib import utils


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
        [n_1_os, n_1_ts],
        [math.ceil(n_1_os / enrolment_ratio), math.ceil(n_1_ts / enrolment_ratio)],
        [n_1_os + math.ceil(n_1_os / enrolment_ratio), n_1_ts + math.ceil(n_1_ts / enrolment_ratio)]
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
        [n_1_os, n_1_ts],
        [math.ceil(n_1_os / enrolment_ratio), math.ceil(n_1_ts / enrolment_ratio)],
        [n_1_os + math.ceil(n_1_os / enrolment_ratio), n_1_ts + math.ceil(n_1_ts / enrolment_ratio)]
    ]


def calculate_power_from_cohens_d(d, n_1, n_2, alpha):
    denominator = (1 / n_1 + 1 / n_2)**0.5
    T_os = t.ppf(q=1 - alpha, df=n_1 + n_2 - 2)
    T_ts = t.ppf(q=1 - alpha/2, df=n_1 + n_2 - 2)
    power_os = t.cdf(x=-T_os + abs(d)/denominator, df=n_1 + n_2 - 2)
    power_ts = t.cdf(x=-T_ts + abs(d)/denominator, df=n_1 + n_2 - 2)

    return [[power_os], [power_ts]]


def calculate_power_from_means(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2, alpha):
    diff = abs(mu_1 - mu_2)
    df = utils.welches_degrees_of_freedom(sigma_1, n_1, sigma_2, n_2)
    denominator = (sigma_1**2 / n_1 + sigma_2**2 / n_2)**0.5
    T_os = t.ppf(q=1 - alpha, df=df)
    T_ts = t.ppf(q=1 - alpha/2, df=df)
    power_os = t.cdf(x=-T_os + diff/denominator, df=df)
    power_ts = t.cdf(x=-T_ts + diff/denominator, df=df)

    return [[power_os], [power_ts]]


def calculate_min_effect_size(n_1, n_2, alpha, power):
    power = power if power < 1 else 0.99999999999
    alpha = alpha if alpha != 0 else 0.0000000001

    # Calculate with Normal distribution
    t_a_one_sided = t.ppf(q=1 - alpha, df=n_1 + n_2 - 2)
    t_a_two_sided = t.ppf(q=1 - alpha/2, df=n_1 + n_2 - 2)
    t_b_one_sided = t.ppf(q=power, df=n_1 + n_2 - 2)

    t_total_os = t_a_one_sided + t_b_one_sided
    t_total_ts = t_a_two_sided + t_b_one_sided

    d_os = t_total_os * (1/n_1 + 1/n_2)**0.5
    d_ts = t_total_ts * (1/n_1 + 1/n_2)**0.5

    return [[d_os], [d_ts]]


def calculate_t_stat_from_cohens_d(d, n_1, n_2):
    n_root = (1/n_1 + 1/n_2)**0.5
    t_stat = d/n_root

    return t_stat


def calculate_t_stat_from_means(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2):
    n_root = (s_1**2 / n_1 + s_2**2/n_2)**0.5
    diff = abs(x_bar_1 - x_bar_2)
    t_stat = diff/n_root

    return t_stat


def calculate_p_value(t_stat, df):
    one_sided_p = 1 - t.cdf(df=df, x=t_stat)
    two_sided_p = 2 * (1 - t.cdf(df=df, x=t_stat))

    return [[one_sided_p], [two_sided_p]]
