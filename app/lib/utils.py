def all_sample_info_provided(sample_inputs):
    all_provided = True
    for sample in sample_inputs:
        for key in sample:
            if sample[key] == "":
                all_provided = False
                break
    return all_provided


def calculate_cohens_d(n_1, n_2, sigma_1, sigma_2):
    mean_diff = abs(n_1 - n_2)
    sd = calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)
    return mean_diff / sd


def calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2):
    return (((n_1 - 1) * sigma_1**2 + (n_2 - 1) * sigma_2**2) / (n_1 + n_2 - 2))**0.5
