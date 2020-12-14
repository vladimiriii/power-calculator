from scipy.stats import norm


def generate_sample_size_notes(alpha, power):
    notes = [
        "r<sub>n</sub> is the ratio of observations, n<sub>1</sub> / n<sub>2</sub>.",
        "The calculation shown is for a two-tailed test. However, from the formula, you can see the only term that will change for a one-sided test is z<sub>1−α/2</sub>​ = {:.3f}, which instead becomes z<sub>1−α</sub>​ = {:.3f}.".format(norm.ppf(1 - alpha/2), norm.ppf(1 - alpha)),
        "The difference in means (or the effect size) for this calculation represents the difference in <i>population</i> means, or the true effect. This is because we are calculating how big a sample we need to have a {:.1%} probability of finding a significant difference (i.e. the 'power' of the experiment) if we repeatedly resampled from these populations.".format(power)
    ]
    return notes


def generate_power_notes(alpha):
    notes = [
        "X is a normally distributed random variable with mean 0 and standard deviation 1: X ~ N(0, 1).",
        "The calculation shown is for a two-tailed test. However, from the formula, you can see the only term that will change for a one-sided test is z<sub>1−α/2</sub>​ = {:.3f}, which instead becomes z<sub>1−α</sub>​ = {:.3f}.".format(norm.ppf(1 - alpha/2), norm.ppf(1 - alpha)),
        "The difference in means (or the effect size) for this calculation represents the difference in <i>population</i> means, or the true effect. This is because we are calculating the probability we will correctly reject H<sub>0</sub> (i.e. the 'power' of the experiment) if we repeatedly resampled from these populations with the specified sample sizes.",
        "Calculating the power of a study based on the observed difference in sample means is not recommended as it will not provide any meaningful information about the power of the study."
    ]
    return notes


def generate_min_effect_size_notes(alpha, power):
    notes = [
        "The calculation shown is for a two-tailed test. However, from the formula, you can see the only term that will change for a one-sided test is z<sub>1−α/2</sub>​ = {:.3f}, which instead becomes z<sub>1−α</sub>​ = {:.3f}.".format(norm.ppf(1 - alpha/2), norm.ppf(1 - alpha)),
        "The minimum effect size produced by this calculation represents the minimum difference in <i>population</i> means that will lead to the correct rejection of H<sub>0</sub> (i.e. a significant difference) in {:.2%} of experiments if we repeatedly resampled from these populations with the specified sample sizes.".format(power)
    ]
    return notes


def generate_t_stat_notes(n_1, n_2, d, t_stat):
    upsilon = n_1 + n_2 - 2
    notes = [
        "The difference in means (or the effect size) for this calculation (d={:.3f}) represents the observed difference in <i>sample</i> means. This is because we are calculating the probability of observing an effect size of {:.3f} or larger if the null hypothesis (H<sub>0</sub>) is true. In other words, the probability that we would incorrectly reject H<sub>0</sub> or the Type I error rate.".format(d, d),
        "The t-statistic can be compared to the critical value for a given level of alpha to assess whether or not to reject H<sub>0</sub>; or it can be used to determine the p-value, which is the probability of observing an effect size at least as large as the one observed if H<sub>0</sub> is true.",
        "The p-value can also be understood as the area underneath the t-distribution where t is greater than {:.3f} for a one-sided test; or greater than {:.3f} <i>and</i> less than {:.3f} for a two-sided test.".format(abs(t_stat), abs(t_stat), -abs(t_stat))
        ]
    return notes


def generate_p_value_notes(n_1, n_2, d, p_one_sided, p_two_sided, t_stat):
    upsilon = n_1 + n_2 - 2
    notes = [
        "T is a t-distributed random variable with {} degrees of freedom: t<sub>υ={}</sub>".format(upsilon, upsilon),
        "The calculation shown is for a two-tailed test. However, from the formula, you can see the only change required for a one-sided test is to not multiply by 2 in the last step.",
        "The difference in means (or the effect size) for this calculation (d={:.3f}) represents the observed difference in <i>sample</i> means. This is because we are calculating the probability of observing an effect size of {:.3f} or larger if the null hypothesis (H<sub>0</sub>) is true. In other words, the probability that we would incorrectly reject H<sub>0</sub> or the Type I error rate.".format(d, d),
        "The p-value can also be understood as the area underneath the t-distribution where t is greater than {:.3f} for a one-sided test (p = {:.3f}); or greater than {:.3f} <i>and</i> less than {:.3f} for a two-sided test (p = {:.3f})".format(abs(t_stat), p_one_sided, abs(t_stat), -abs(t_stat), p_two_sided)
    ]
    return notes


def generate_power_distributions_text(alpha, power, mu_1, sigma_1, mu_2, sigma_2, pooled_sd):
    text = [
        "The chart to the right shows two hypothetical distributions of the differences in sample means. The red function is the expected distribution of the difference in the means of two samples drawn from one population, N(μ=0, σ={:.3f}). This represents the null hypothesis (H<sub>0</sub>: μ<sub>1</sub>=μ<sub>2</sub>).".format(pooled_sd),
        "The blue function is the expected distribution of the difference in the means of samples drawn from two different populations, N(μ<sub>1</sub>={:.3f}, σ<sub>1</sub>={:.3f}) and N(μ<sub>2</sub>={:.3f}, σ<sub>2</sub>={:.3f}). This represents the alternative hypothesis (H<sub>A</sub>: μ<sub>2</sub>-μ<sub>1</sub>={:.3f}).".format(mu_1, sigma_1, mu_2, sigma_2, mu_2 - mu_1),
        "The areas shaded in red represent the probability of observing differences in sample means that would lead to a rejection of H<sub>0</sub> at the {:.2f} level of significance (for a two-tailed test). I.e. the shaded area represents {:.1%} of the total area under the null hypothesis distribution.".format(alpha, alpha),
        "The area shaded in blue represents the probability of observing differences in sample means that would lead to a failure to reject of H<sub>0</sub> as they were found not to be statistically significant. This area represents {:.1%} of the total area under the alternative hypothesis distribution.".format(1 - power)
    ]
    return text


def generate_test_distribution_text(alpha, n_1, n_2, df):
    text = [
        "The chart to the right shows the distribution of a t-statistic, t(υ={}), which is a function of the difference in the means of two samples (n<sub>1</sub>={}, n<sub>2</sub>={}).".format(df, n_1, n_2),
        "The areas shaded in red represent the probability of observing differences in sample means that would lead to a rejection of H<sub>0</sub> at the {:.2f} level of significance (for a two-tailed test). I.e. the shaded area represents {:.1%} of the total area under the null hypothesis distribution.".format(alpha, alpha)
    ]
    return text
