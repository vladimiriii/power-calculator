from scipy.stats import norm, t, ttest_ind, ttest_ind_from_stats
import math
from app.lib import utils


def create_sample_size_from_means_formula(mu_1, mu_2, sigma_1, sigma_2, alpha, power, enrolment_ratio):
    formulae = []
    step_1 = "n_1 = \\frac{{(\\sigma_1^2 + r_n\\sigma_2^2)(z_{{1 - \\alpha/2}} + z_{{1 - \\beta}})^2}}{{(\\mu_1 - \\mu_2)^2}}"
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

    step_4 = "n_2 = \\frac{{n_1}}{{r_n}} = \\frac{{{}}}{{{:.3f}}} = {}"
    formulae.append(step_4.format(n_1, enrolment_ratio, math.ceil(n_1 / enrolment_ratio)))

    return formulae


def create_sample_size_from_d_formula(d, alpha, power, enrolment_ratio):
    formulae = []
    step_1 = "n_1 =  \\frac{{(1 + r_n)(z_{{1 - \\alpha/2}} + z_{{1 - \\beta}})^2}}{{d^2}}"
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

    step_4 = "n_2 = \\frac{{n_1}}{{r_n}} = \\frac{{{}}}{{{:.3f}}} = {}"
    formulae.append(step_4.format(n_1, enrolment_ratio, math.ceil(n_1 / enrolment_ratio)))

    return formulae


def create_power_from_means_formula(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2, alpha):
    formulae = []
    df = int(utils.welches_degrees_of_freedom(sigma_1, n_1, sigma_2, n_2))
    sig = 1 - alpha/2
    t_crit = t.ppf(q=sig, df=df)
    step_1 = "t_{{crit}} = t_{{1-\\alpha/2, \ \\upsilon}} = t_{{{:.3f}, \ {}}} = {:.3f}"
    formulae.append(step_1.format(sig, df, t_crit))

    step_2 = "\\beta = P(T <= t_{{crit}})\ where\ T\ \\sim\ t_{{\\upsilon={},\ \\mu={:.3f}}}"
    d = utils.calculate_cohens_d(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2)
    nc = abs(d) * (2 / (1/n_1 + 1/n_2) / 2)**0.5
    formulae.append(step_2.format(df, nc))

    nct_dist = utils.initialize_nct_distribution(df=df, nc=nc)
    beta = nct_dist.cdf(x=t_crit)
    step_3 = "\\beta = P(T <= {:.3f}) = {:.3f}"
    formulae.append(step_3.format(t_crit, beta))

    step_4 = "1 - \\beta = 1 - {:.3f} = {:.3f}"
    formulae.append(step_4.format(beta, 1 - beta))

    return formulae


def create_power_from_d_formula(d, n_1, n_2, alpha):
    formulae = []
    df = n_1 + n_2 - 2
    sig = 1 - alpha/2
    t_crit = t.ppf(q=sig, df=df)
    step_1 = "t_{{crit}} = t_{{1-\\alpha/2, \ \\upsilon}} = t_{{{:.3f}, \ {}}} = {:.3f}"
    formulae.append(step_1.format(sig, df, t_crit))

    step_2 = "\\beta = P(T <= t_{{crit}})\ where\ T\ \\sim\ t_{{\\upsilon={},\ \\mu={:.3f}}}"
    nc = abs(d) * (2 / (1/n_1 + 1/n_2) / 2)**0.5
    formulae.append(step_2.format(df, nc))

    nct_dist = utils.initialize_nct_distribution(df=df, nc=nc)
    beta = nct_dist.cdf(x=t_crit)
    step_3 = "\\beta = P(T <= {:.3f}) = {:.3f}"
    formulae.append(step_3.format(t_crit, beta))

    step_4 = "1 - \\beta = 1 - {:.3f} = {:.3f}"
    formulae.append(step_4.format(beta, 1 - beta))

    return formulae


def create_min_effect_size_formula(alpha, power, n_1, n_2):
    formulae = []
    step_1 = "d_{{min}} = (t_{{1-\\alpha/2,\ \\upsilon}} + t_{{1-\\beta,\ \\upsilon}}) \\cdot \\sqrt{{(\\frac{{1}}{{n_1}} + \\frac{{1}}{{n_2}})}}"
    formulae.append(step_1)

    step_2 = "d_{{min}} = (t_{{{:.3f},\ {}}} + t_{{{:.3f},\ {}}}) \\cdot \\sqrt{{(\\frac{{1}}{{{}}} + \\frac{{1}}{{{}}})}}"
    df = n_1 + n_2 - 2
    formulae.append(step_2.format(1 - alpha/2, df, power, df, n_1, n_2))

    step_3 = "d_{{min}} = ({:.3f} + {:.3f})\\cdot\\sqrt{{{:.3f}}}"
    n_ratio = 1/n_1 + 1/n_2
    t_a = t.ppf(q=1 - alpha/2, df=df)
    t_b = t.ppf(q=power, df=df)
    formulae.append(step_3.format(t_a, t_b, n_ratio))

    step_4 = "d_{{min}} = {:.3f} \\times {:.3f} = {:.3f}"
    sqrt_n_ratio = n_ratio**0.5
    t_total = t_a + t_b
    min_effect = t_total * sqrt_n_ratio
    formulae.append(step_4.format(t_total, sqrt_n_ratio, min_effect))

    return formulae


def create_t_stat_from_means_formula(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2):
    formulae = []
    step_1 = "t = \\frac{{|\\bar{{x_1}} - \\bar{{x_2}}|}}{{\\sqrt{{\\frac{{s_1^2}}{{n_1}} + \\frac{{s_2^2}}{{n_2}}}}}}"
    formulae.append(step_1)

    step_2 = "t = \\frac{{|{:.3f} - {:.3f}|}}{{\\sqrt{{\\frac{{{:.3f}^2}}{{{}}} + \\frac{{{:.3f}^2}}{{{}}}}}}}"
    formulae.append(step_2.format(x_bar_1, x_bar_2, s_1, n_1, s_2, n_2))

    step_3 = "t = \\frac{{{:.3f}}}{{{:.3f}}} = {:.3f}"
    numerator = abs(x_bar_1 - x_bar_2)
    denominator = (s_1**2 / n_1 + s_2**2 / n_2)**0.5
    t_stat = numerator / denominator
    formulae.append(step_3.format(numerator, denominator, t_stat))

    return formulae


def create_t_stat_from_d_formula(d, n_1, n_2):
    formulae = []
    step_1 = "t = \\frac{{|d|}}{{\\sqrt{{\\frac{{1}}{{n_1}} + \\frac{{1}}{{n_2}}}}}}"
    formulae.append(step_1)

    step_2 = "t = \\frac{{|{:.3f}|}}{{\\sqrt{{\\frac{{1}}{{{}}} + \\frac{{1}}{{{}}}}}}}"
    formulae.append(step_2.format(d, n_1, n_2))

    step_3 = "t = \\frac{{{:.3f}}}{{{:.3f}}} = {:.3f}"
    diff = abs(d)
    n_root = (1/n_1 + 1/n_2)**0.5
    t_crit = diff / n_root
    formulae.append(step_3.format(diff, n_root, t_crit))

    return formulae


def create_p_value_from_means_formula(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2):
    formulae = []
    step_1 = "t = \\frac{{|\\bar{{x_1}} - \\bar{{x_2}}|}}{{\\sqrt{{\\frac{{s_1^2}}{{n_1}} + \\frac{{s_2^2}}{{n_2}}}}}}"
    formulae.append(step_1)

    step_2 = "t = \\frac{{|{:.3f} - {:.3f}|}}{{\\sqrt{{\\frac{{{:.3f}^2}}{{{}}} + \\frac{{{:.3f}^2}}{{{}}}}}}}"
    formulae.append(step_2.format(x_bar_1, x_bar_2, s_1, n_1, s_2, n_2))

    step_3 = "t = \\frac{{{:.3f}}}{{{:.3f}}} = {:.3f}"
    numerator = abs(x_bar_1 - x_bar_2)
    denominator = (s_1**2 / n_1 + s_2**2 / n_2)**0.5
    t_stat = numerator / denominator
    formulae.append(step_3.format(numerator, denominator, t_stat))

    p_value = 2 * (1 - t.cdf(t_stat, df=utils.welches_degrees_of_freedom(s_1, n_1, s_2, n_2)))
    step_4 = "p = 2 \\times P(T > {:.3f}) = {:.3f}"
    formulae.append(step_4.format(t_stat, p_value))

    return formulae


def create_p_value_from_d_formula(d, n_1, n_2):
    formulae = []
    step_1 = "t = \\frac{{|d|}}{{\\sqrt{{\\frac{{1}}{{n_1}} + \\frac{{1}}{{n_2}}}}}}"
    formulae.append(step_1)

    step_2 = "t = \\frac{{|{:.3f}|}}{{\\sqrt{{\\frac{{1}}{{{}}} + \\frac{{1}}{{{}}}}}}}"
    formulae.append(step_2.format(d, n_1, n_2))

    step_3 = "t = \\frac{{{:.3f}}}{{{:.3f}}} = {:.3f}"
    diff = abs(d)
    n_root = (1/n_1 + 1/n_2)**0.5
    t_stat = diff / n_root
    formulae.append(step_3.format(diff, n_root, t_stat))

    df = n_1 + n_2 - 2
    p_value = 2 * (1 - t.cdf(t_stat, df=df))
    step_4 = "p = 2 \\times P(T > {:.3f}) = {:.3f}"
    formulae.append(step_4.format(t_stat, p_value))

    return formulae
