from scipy.stats import norm, t, ttest_ind, ttest_ind_from_stats
import math
from app.lib import utils


def create_sample_size_from_means_formula(mu_1, mu_2, sigma_1, sigma_2, alpha, power, enrolment_ratio):
    formulae = []
    step_1 = "n_1 = \\frac{{(\\sigma_1^2 + r_e\\sigma_2^2)(z_{{1 - \\alpha/2}} + z_{{1 - \\beta}})^2}}{{(\\mu_1 - \\mu_2)^2}}"
    formulae.append(step_1)

    z_a = norm.ppf(1 - alpha/2)
    z_b = norm.ppf(power)

    step_2 = "n_1 = \\frac{{({:.3f}^2 + {:.3f}\\times{:.3f}^2)({:.3f} + {:.3f})^2}}{{({:.3f} - {:.3f})^2}}"
    formulae.append(step_2.format(sigma_1, enrolment_ratio, sigma_2, z_a, z_b, mu_1, mu_2))

    step_3 = "n_1 = \\frac{{{:.3f}\\times{:.3f}}}{{{:.3f}}} = {}"
    numerator_1 = sigma_1**2 + enrolment_ratio * sigma_2**2
    numerator_2 = (z_a + z_b)**2
    denominator = (mu_1 - mu_2)**2
    n_1 = math.ceil(numerator_1 * numerator_2 / denominator)
    formulae.append(step_3.format(numerator_1, numerator_2, denominator, n_1))

    step_4 = "n_2 = \\frac{{n_1}}{{r_e}} = \\frac{{{}}}{{{:.3f}}} = {}"
    formulae.append(step_4.format(n_1, enrolment_ratio, math.ceil(n_1 / enrolment_ratio)))

    return formulae


def create_sample_size_from_d_formula(d, alpha, power, enrolment_ratio):
    formulae = []
    step_1 = "n_1 =  \\frac{{(1 + r_e)(z_{{1 - \\alpha/2}} + z_{{1 - \\beta}})^2}}{{d^2}}"
    formulae.append(step_1)

    z_a = norm.ppf(1 - alpha/2)
    z_b = norm.ppf(power)

    step_2 = "n_1 = \\frac{{(1 + {:.3f})({:.3f} + {:.3f})^2}}{{{:.3f}^2}}"
    formulae.append(step_2.format(enrolment_ratio, z_a, z_b, d))

    step_3 = "n_1 = \\frac{{{:.3f}\\times{:.3f}}}{{{:.3f}}} = {}"
    numerator_1 = 1 + enrolment_ratio
    numerator_2 = (z_a + z_b)**2
    denominator = d**2
    n_1 = math.ceil(numerator_1 * numerator_2 / denominator)
    formulae.append(step_3.format(numerator_1, numerator_2, denominator, n_1))

    step_4 = "n_2 = \\frac{{n_1}}{{r_e}} = \\frac{{{}}}{{{:.3f}}} = {}"
    formulae.append(step_4.format(n_1, enrolment_ratio, math.ceil(n_1 / enrolment_ratio)))

    return formulae


def create_power_from_means_formula(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2, alpha):
    formulae = []
    step_1 = "z_{{crit}} = -z_{{1-\\alpha/2}} + \\frac{{|\\mu_1 - \\mu_2|}}{{\\sqrt{{\\sigma_1^2/n_1 + \\sigma_2^2/n_2}}}}"
    formulae.append(step_1)

    z_a = norm.ppf(1 - alpha/2)
    step_2 = "z_{{crit}} = -{:.3f} + \\frac{{|{:.3f} - {:.3f}|}}{{\\sqrt{{\\frac{{{:.3f}^2}}{{{}}} + \\frac{{{:.3f}^2}}{{{}}}}}}}"
    formulae.append(step_2.format(z_a, mu_1, mu_2, sigma_1, n_1, sigma_2, n_2))

    step_3 = "z_{{crit}} = -{:.3f} + \\frac{{{:.3f}}}{{\\sqrt{{{:.3f}}}}} = {:.3f}"
    diff = abs(mu_1 - mu_2)
    pooled_variance = sigma_1**2/n_1 + sigma_2**2/n_2
    z_crit = -z_a + (diff / pooled_variance**0.5)
    formulae.append(step_3.format(z_a, diff, pooled_variance, z_crit))

    power = norm.cdf(z_crit)
    step_4 = "1 - \\beta = P(X <= {:.3f}) = {:.3f}"
    formulae.append(step_4.format(z_crit, power))

    return formulae


def create_power_from_d_formula(d, n_1, n_2, alpha):
    formulae = []
    step_1 = "z_{{crit}} = -z_{{1-\\alpha/2}} + \\frac{{|d|}}{{\\sqrt{{1/n_1 + 1/n_2}}}}"
    formulae.append(step_1)

    z_a = norm.ppf(1 - alpha/2)
    step_2 = "z_{{crit}} = -{:.3f} + \\frac{{|{:.3f}|}}{{\\sqrt{{1/{} + 1/{}}}}}"
    formulae.append(step_2.format(z_a, d, n_1, n_2))

    step_3 = "z_{{crit}} = -{:.3f} + \\frac{{{:.3f}}}{{\\sqrt{{{:.3f}}}}} = {:.3f}"
    diff = abs(d)
    df = 1/n_1 + 1/n_2
    z_crit = -z_a + (diff / df**0.5)
    formulae.append(step_3.format(z_a, diff, df, z_crit))

    power = norm.cdf(z_crit)
    step_4 = "1 - \\beta = P(X <= {:.3f}) = {:.3f}"
    formulae.append(step_4.format(z_crit, power))

    return formulae


def create_p_value_from_means_formula(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2):
    formulae = []
    step_1 = "t_{{crit}} = \\frac{{|\\mu_1 - \\mu_2|}}{{\\left(\\frac{{\\sigma_1^2(n_1 - 1) + \\sigma_2^2(n_2 - 1)}}{{n_1 + n_2 - 2}}\\right)\\cdot\\sqrt{{\\frac{{1}}{{n_1}} + \\frac{{1}}{{n_2}}}}}}"
    formulae.append(step_1)

    step_2 = "t_{{crit}} = \\frac{{|{:.3f} - {:.3f}|}}{{\\left(\\frac{{{:.3f}^2({} - 1) + {:.3f}^2({} - 1)}}{{{} + {} - 2}}\\right)\\cdot\\sqrt{{\\frac{{1}}{{{}}} + \\frac{{1}}{{{}}}}}}}"
    formulae.append(step_2.format(mu_1, mu_2, sigma_1, n_1, sigma_2, n_2, n_1, n_2, n_1, n_2))

    step_3 = "t_{{crit}} = \\frac{{{:.3f}}}{{{:.3f}\\times{:.3f}}} = {:.3f}"
    diff = abs(mu_1 - mu_2)
    std_pooled = utils.calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)
    n_root = (1/n_1 + 1/n_2)**0.5
    t_crit = diff / (std_pooled * n_root)
    formulae.append(step_3.format(diff, std_pooled, n_root, t_crit))

    p_value = 2 * (1 - t.cdf(t_crit, df=utils.welches_degrees_of_freedom(sigma_1, n_1, sigma_2, n_2)))
    step_4 = "p = 2 \\times P(T > {:.3f}) = {:.3f}"
    formulae.append(step_4.format(t_crit, p_value))

    return formulae


def create_p_value_from_d_formula(d, n_1, n_2):
    formulae = []
    step_1 = "t_{{crit}} = \\frac{{|d|}}{{\\sqrt{{\\frac{{1}}{{n_1}} + \\frac{{1}}{{n_2}}}}}}"
    formulae.append(step_1)

    step_2 = "t_{{crit}} = \\frac{{|{:.3f}|}}{{\\sqrt{{\\frac{{1}}{{{}}} + \\frac{{1}}{{{}}}}}}}"
    formulae.append(step_2.format(d, n_1, n_2))

    step_3 = "t_{{crit}} = \\frac{{{:.3f}}}{{{:.3f}}} = {:.3f}"
    diff = abs(d)
    n_root = (1/n_1 + 1/n_2)**0.5
    t_crit = diff / n_root
    formulae.append(step_3.format(diff, n_root, t_crit))

    df = n_1 + n_2 - 2
    p_value = 2 * (1 - t.cdf(t_crit, df=df))
    step_4 = "p = 2 \\times P(T > {:.3f}) = {:.3f}"
    formulae.append(step_4.format(t_crit, p_value))

    return formulae



# min_effect_size = r"d_{min} = \sqrt{\frac{(1 + \frac{n_1}{n_2})(t_{1-\alpha/2} + t_{1-\beta})^2}{n_1}}"
