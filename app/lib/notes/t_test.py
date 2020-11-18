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


def generate_p_value_notes(n_1, n_2):
    upsilon = n_1 + n_2 - 2
    notes = [
        "T is a t distributed random variable with {} degrees of freedom: t<sub>υ={}</sub>".format(upsilon, upsilon),
        "The calculation shown is for a two tailed test. However, from the forumla, you can see the only change required for a one-sided test is to not multiply by 2 in the last step.",
        "The difference in means (or the effect size) for this calculation represents the observed difference in <i>sample</i> means. This is because we are calculating the probability of observing an effect size at least as large as the one observed if H<sub>0</sub> is true. That is, it is the probability that we would incorrectly reject H<sub>0</sub> (i.e. the Type I error rate)."
    ]
    return notes
