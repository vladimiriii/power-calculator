import math


def all_sample_info_provided(sample_inputs):
    all_provided = True
    for sample in sample_inputs:
        for key in sample:
            if sample[key] == "":
                all_provided = False
                break
    return all_provided


def calculate_cohens_d(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2):
    mean_diff = abs(mu_1 - mu_2)
    sd = calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)
    return mean_diff / sd


def calculate_sample_size_adjustment(n_1, n_2):
    return (n_1 + n_2) / (n_1 + n_2 - 2)


def calculate_d_adjustment(s_1, n_1, s_2, n_2):
    ss_adjust = calculate_sample_size_adjustment(n_1, n_2)
    sd_adjust = ((n_1 - 1)*s_1**2 + (n_2 - 1)*s_2**2) / (n_2 * s_1**2 + n_1 * s_2**2)
    return (ss_adjust * sd_adjust)**0.5


def calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2):
    return (((n_1 - 1) * sigma_1**2 + (n_2 - 1) * sigma_2**2) / (n_1 + n_2 - 2))**0.5


def determine_decimal_points(x):
    return int(round(max(4 + (-1 * math.log(abs(x), 10)), 0), 0))


def welches_degrees_of_freedom(sigma_1, n_1, sigma_2, n_2):
    return (sigma_1**2/n_1 + sigma_2**2/n_2)**2 / ((sigma_1**2/n_1)**2/(n_1-1) + (sigma_2**2/n_2)**2/(n_2-1))


def find_closest_value(lst, x):
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - x))]
