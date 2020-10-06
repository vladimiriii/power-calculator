

def calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2):
    return (((n_1 - 1) * sigma_1**2 + (n_2 - 1) * sigma_2**2) / (n_1 + n_2 - 2))**0.5
