from scipy.stats import norm, t, ttest_ind, ttest_ind_from_stats
import math
from app.lib import utils


def generate_formulas(inputs):
    results = {}
    sample_fields = inputs['sampleFields']
    if inputs['target'] == "sample-size":
        if utils.all_sample_info_provided(sample_fields):
            results['formulae'] = create_sample_size_from_means_formula(mu_1=float(sample_fields[0]['mean']),
                                                                        mu_2=float(sample_fields[1]['mean']),
                                                                        sigma_1=float(sample_fields[0]['stdDev']),
                                                                        sigma_2=float(sample_fields[1]['stdDev']),
                                                                        alpha=float(inputs['alpha']),
                                                                        power=float(inputs['power']),
                                                                        enrolment_ratio=float(inputs['enrolmentRatio']))
        else:
            results['formulae'] = create_sample_size_from_d_formula(d=float(inputs['effectSize']),
                                                                    alpha=float(inputs['alpha']),
                                                                    power=float(inputs['power']),
                                                                    enrolment_ratio=float(inputs['enrolmentRatio']))
        results['notes'] = generate_sample_size_notes(float(inputs['alpha']), float(inputs['power']))
    elif inputs['target'] == "power":
        if utils.all_sample_info_provided(sample_fields):
            results['formulae'] = create_power_from_means_formula(mu_1=float(sample_fields[0]['mean']),
                                                                  sigma_1=float(sample_fields[0]['stdDev']),
                                                                  n_1=int(sample_fields[0]['n']),
                                                                  mu_2=float(sample_fields[1]['mean']),
                                                                  sigma_2=float(sample_fields[1]['stdDev']),
                                                                  n_2=int(sample_fields[1]['n']),
                                                                  alpha=float(inputs['alpha']))
        else:
            results['formulae'] = create_power_from_d_formula(d=float(inputs['effectSize']),
                                                              n_1=int(sample_fields[0]['n']),
                                                              n_2=int(sample_fields[1]['n']),
                                                              alpha=float(inputs['alpha']))
        results['notes'] = generate_power_notes(float(inputs['alpha']))

    elif inputs['target'] == "p-value":
        if utils.all_sample_info_provided(sample_fields):
            results['formulae'] = create_p_value_from_means_formula(mu_1=float(sample_fields[0]['mean']),
                                                                    sigma_1=float(sample_fields[0]['stdDev']),
                                                                    n_1=int(sample_fields[0]['n']),
                                                                    mu_2=float(sample_fields[1]['mean']),
                                                                    sigma_2=float(sample_fields[1]['stdDev']),
                                                                    n_2=int(sample_fields[1]['n']))
        else:
            results['formulae'] = create_p_value_from_d_formula(d=float(inputs['effectSize']),
                                                                n_1=int(sample_fields[0]['n']),
                                                                n_2=int(sample_fields[1]['n']))
        results['notes'] = generate_p_value_notes(int(sample_fields[0]['n']), int(sample_fields[1]['n']))
    # elif inputs['target'] == "min-effect":
    #     if utils.all_sample_info_provided(sample_fields):
    #         results = caclulate_min_effect_size(n_1=float(sample_fields[0]['n']),
    #                                             n_2=float(sample_fields[1]['n']),
    #                                             alpha=float(inputs['alpha']),
    #                                             power=float(inputs['power']))
    else:
        results['formulae'] = []
        results['notes'] = []

    return results


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


def generate_sample_size_notes(alpha, power):
    notes = [
        "r<sub>e</sub> is the enrolment ratio.",
        "The calculation shown is for a two tailed test. However, from the forumla, you can see the only term that will change for a one-sided test is z<sub>1−α/2</sub>​ = {:.3f}, which instead becomes z<sub>1−α</sub>​ = {:.3f}.".format(norm.ppf(1 - alpha/2), norm.ppf(1 - alpha)),
        "The difference in means (or the effect size) for this calculation represents the difference in <i>population</i> means, or the true effect. This is because we are calculating how big a sample we need to detect this difference in {:.1%} of experiments if we repeatedly resampled from these populations (i.e. the 'power' of the experiment).".format(power)
    ]
    return notes


def generate_power_notes(alpha):
    notes = [
        "X is a normally distributed random variable with mean 0 and standard deviation 1: X ~ N(0, 1).",
        "The calculation shown is for a two tailed test. However, from the forumla, you can see the only term that will change for a one-sided test is z<sub>1−α/2</sub>​ = {:.3f}, which instead becomes z<sub>1−α</sub>​ = {:.3f}.".format(norm.ppf(1 - alpha/2), norm.ppf(1 - alpha)),
        "The difference in means (or the effect size) for this calculation represents the difference in <i>population</i> means, or the true effect. This is because we are calculating the probability we will correctly reject H<sub>0</sub> (i.e. the 'power' of the experiment) if we repeatedly resampled from these populations with the specified sample sizes.",
        "Calculating the power of a study based on the observed difference in sample means is not recommended as it will not provide any meaningful information about the power of the study."
    ]
    return notes


def generate_p_value_notes(n_1, n_2):
    upsilon = n_1 + n_2 - 2
    notes = [
        "T is a t distributed random variable with {} degrees of freedom: t<sub>υ={}</sub>".format(upsilon, upsilon),
        "The calculation shown is for a two tailed test. However, from the forumla, you can see the only change required for a one-sided test is to not multiply by 2 in the last step.",
        "The difference in means (or the effect size) for this calculation represents the observed difference in <i>sample</i> means. This is because we are calculating the probability of observing an effect size at least as large as the one observed if H<sub>0</sub> is true. That is, it is the probability that we would incorrectly reject H<sub>0</sub> (i.e. the Type I error rate)."
    ]
    return notes



# min_effect_size = r"d_{min} = \sqrt{\frac{(1 + \frac{n_1}{n_2})(t_{1-\alpha/2} + t_{1-\beta})^2}{n_1}}"
