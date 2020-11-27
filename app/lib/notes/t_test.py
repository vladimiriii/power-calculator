from scipy.stats import norm


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


def generate_min_effect_size_notes(alpha, power):
    notes = [
        "The calculation shown is for a two tailed test. However, from the forumla, you can see the only term that will change for a one-sided test is z<sub>1−α/2</sub>​ = {:.3f}, which instead becomes z<sub>1−α</sub>​ = {:.3f}.".format(norm.ppf(1 - alpha/2), norm.ppf(1 - alpha)),
        "The minimum effect size produced by this calculation represents the minimum difference in <i>population</i> means that will lead to the correct rejection of H<sub>0</sub> in {:.2%} of experiments if we repeatedly resampled from these populations with the specified sample sizes.".format(power)
    ]
    return notes


def generate_t_stat_notes(n_1, n_2, d, t_stat):
    upsilon = n_1 + n_2 - 2
    notes = [
        "The difference in means (or the effect size) for this calculation (d={:.3f}) represents the observed difference in <i>sample</i> means. This is because we are calculating the probability of observing an effect size at least as large as the one observed if H<sub>0</sub> is true. That is, the probability that we would incorrectly reject H<sub>0</sub> or the Type I error rate.".format(d),
        "The t-statistic can be compared to the critical value for a given level of alpha to decide if H<sub>0</sub> is rejected; or it can be used to determine the p-value, which is the probability of observing an effect size at least as large as the one observed if H<sub>0</sub> is true.",
        "The p-value can also be understood as the area underneath the t-distribution shown above where t is greater than {:.3f} for a one-sided test; or greater than {:.3f} <i>and</i> less than {:.3f} for a two-sided test.".format(abs(t_stat), abs(t_stat), -abs(t_stat))
        ]
    return notes


def generate_p_value_notes(n_1, n_2, d, p_one_sided, p_two_sided, t_stat):
    upsilon = n_1 + n_2 - 2
    notes = [
        "T is a t-distributed random variable with {} degrees of freedom: t<sub>υ={}</sub>".format(upsilon, upsilon),
        "The calculation shown is for a two tailed test. However, from the forumla, you can see the only change required for a one-sided test is to not multiply by 2 in the last step.",
        "The difference in means (or the effect size) for this calculation (d={:.3f}) represents the observed difference in <i>sample</i> means. This is because we are calculating the probability of observing an effect size at least as large as the one observed if H<sub>0</sub> is true. That is, the probability that we would incorrectly reject H<sub>0</sub> or the Type I error rate.".format(d),
        "The p-value can also be understood as the area underneath the t-distribution where t is greater than {:.3f} for a one-sided test (p = {:.3f}); or greater than {:.3f} <i>and</i> less than {:.3f} for a two-sided test (p = {:.3f})".format(abs(t_stat), p_one_sided, abs(t_stat), -abs(t_stat), p_two_sided)
    ]
    return notes
