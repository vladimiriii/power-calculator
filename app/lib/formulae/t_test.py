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
            results['formulae'] = []
            # results = calculate_sample_size_from_cohens_d(d=float(inputs['effectSize']),
            #                                               alpha=float(inputs['alpha']),
            #                                               power=float(inputs['power']),
            #                                               enrolment_ratio=float(inputs['enrolmentRatio']))
        results['notes'] = generate_sample_size_notes(float(inputs['alpha']), float(inputs['power']))
    else:
        results['formulae'] = []
        results['notes'] = []
    # elif inputs['target'] == "power":
    #     if utils.all_sample_info_provided(sample_fields):
    #         results = calculate_power_from_means(mu_1=float(sample_fields[0]['mean']),
    #                                              sigma_1=float(sample_fields[0]['stdDev']),
    #                                              n_1=float(sample_fields[0]['n']),
    #                                              mu_2=float(sample_fields[1]['mean']),
    #                                              sigma_2=float(sample_fields[1]['stdDev']),
    #                                              n_2=float(sample_fields[1]['n']),
    #                                              alpha=float(inputs['alpha']))
    #     else:
    #         results = calculate_power_from_cohens_d(d=float(inputs['effectSize']),
    #                                                 n_1=float(sample_fields[0]['n']),
    #                                                 n_2=float(sample_fields[1]['n']),
    #                                                 alpha=float(inputs['alpha']))
    #
    # elif inputs['target'] == "p-value":
    #     if utils.all_sample_info_provided(sample_fields):
    #         results = caclulate_p_value_from_means(mu_1=float(sample_fields[0]['mean']),
    #                                                sigma_1=float(sample_fields[0]['stdDev']),
    #                                                n_1=float(sample_fields[0]['n']),
    #                                                mu_2=float(sample_fields[1]['mean']),
    #                                                sigma_2=float(sample_fields[1]['stdDev']),
    #                                                n_2=float(sample_fields[1]['n']))
    #     else:
    #         results = caclulate_p_value_from_cohens_d(d=float(inputs['effectSize']),
    #                                                   n_1=float(sample_fields[0]['n']),
    #                                                   n_2=float(sample_fields[1]['n']))
    # elif inputs['target'] == "min-effect":
    #     if utils.all_sample_info_provided(sample_fields):
    #         results = caclulate_min_effect_size(n_1=float(sample_fields[0]['n']),
    #                                             n_2=float(sample_fields[1]['n']),
    #                                             alpha=float(inputs['alpha']),
    #                                             power=float(inputs['power']))

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


def generate_sample_size_notes(alpha, power):
    notes = [
        "r<sub>e</sub> is the enrolment ratio.",
        "The calculation shown is for a two tailed test. However, from the forumla, you can see the only term that will change for a one-sided test is z<sub>1−α/2</sub>​ = {:.3f}, which instead becomes z<sub>1−α</sub>​ = {:.3f}.".format(norm.ppf(1 - alpha/2), norm.ppf(1 - alpha)),
        "The difference in means (or the effect size) for this calculation represents the difference in <i>population</i> means, or the true effect. This is because we are calculating how big a sample we need to detect this difference in {:.1%} of experiments if we repeatedly resampled from these populations (i.e. the 'power' of the experiment).".format(power)
    ]
    return notes


# sample_size_from_d = r"s_1 =  \frac{(1 + \frac{n_1}{n_2})(z_\alpha + z_\beta)^2}{d^2}"
# sample_size_from_means = r"s_1 =  \frac{(\sigma_1^2 + \frac{n_1}{n_2}\cdot\sigma_2^2)(z_\alpha + z_\beta)^2}{(\mu_1 - \mu_2)^2}"
# power_t_crit_from_d = r"t_{crit} = -t_{1-\alpha/2}\cdot\frac{|d|}{\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}"
# power_t_crit_from_means = r"t_{crit} =  -t_{1-\alpha/2}\cdot\frac{|\mu_1 - \mu_2|}{\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}}}"
# p_value_t_crit_from_d = r"t_{crit} =  \frac{|d|}{\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}"
# p_value_t_crit_from_means = r"t_{crit} =  \frac{|\mu_1 - \mu_2|}{\left(\frac{\sigma_1^2(n_1 - 1) + \sigma_2^2(n_2 - 1)}{n_1 + n_2 - 2}\right)\cdot\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}"
# min_effect_size = r"d_{min} = \sqrt{\frac{(1 + \frac{n_1}{n_2})(t_{1-\alpha/2} + t_{1-\beta})^2}{n_1}}"
