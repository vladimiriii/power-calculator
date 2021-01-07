js_folder = "ttest2ind"
header_text = "t-test: Two Independent Samples"


def generate_when_to_use_text():
    return """
        <p>A t-test is any hypothesis test where the test statistic follows a <a href="https://en.wikipedia.org/wiki/Student%27s_t-distribution" target="_blank">Student's t-distribution</a>. In this version of a t-test, we are testing the probability that two independent samples were drawn from the same population based on the means (and variances) of those samples. More specifically, this version of a t-test is used when:</p>
        <ol>
            <li>You have two independent samples. E.g. a treatment group and a control group, not a before and after treatment comparison ("paired samples").</li>
            <li>You want to assess if a treatment led to some measureable difference in the groups (e.g. giving the treatment group a low fat diet led to a reduction in average weight).</li>
            <li>You do not know the population standard deviation(s). If you do, you can instead use a <i>z</i>-test.</li>
        </ol>
        """


def generate_options_text():
    return """
        <p>You can use this calculator to estimate:</p>
        <ol>
            <li>What sample size a planned study will need to detect an effect size at a given power level?</li>
            <li>How much power will a planned study have based on my expected sample and effect sizes?<sup>1</sup></li>
            <li>What is the smallest effect size a planned study can detect for a given power level and sample size?</li>
            <li>What is the t-statistic and/or p-value for a completed study?</li>
        </ol>
        <p>[1] It is a common mistake to try to calculate the power of a completed study based on the <i>observed</i> effect size. You need to know (or estimate) the true effect size to calculate the power of a study.</p>
    """


def generate_assumptions_text():
    return """
        <p>When conducting a t-test with two independent samples, the following assumptions are made about your data:</p>
        <ol>
            <li>Your data consists of two <a href="https://en.wikipedia.org/wiki/Independent_and_identically-distributed_random_variables" target="_blank">independent and identically distributed</a> samples, one from each of the two populations being compared (although they may turn out to be the same population).</li>
            <li>The sample means (<span style="text-decoration:overline;"><i>X</i></span><sub>1</sub> and <span style="text-decoration:overline;"><i>X</i></span><sub>2</sub>) are normally distributed.<sup>1</sup></li>
            <li>The sample variances (<i>s</i><sup>2</sup><sub>1</sub> and <i>s</i><sup>2</sup><sub>2</sub>) are χ<sup>2</sup> distributed.<sup>2</sup></li>
            <li>The sample means and sample variances are statistically independent.</li>
            <li>This calculator does not require the groups to have equal variance as it uses the Welch's unequal variances t-test formulation by default<sup>3</sup></li>
        </ol>
        <br>
        <p>[1] This does not require your underlying data to be normally distributed. With larger samples, the <a href="https://en.wikipedia.org/wiki/Central_limit_theorem" target='_blank'>Central Limit Theorem</a> typically means the sample means will be normally distributed.</p>
        <p>[2] This assumption holds if the underlying data are normally distributed, but not neccessarily if you are relying on the Central Limit Theorem for normally distributed sample means.</p>
        <p>[3] <a href='https://daniellakens.blogspot.com/2015/01/always-use-welchs-t-test-instead-of.html' target='_blank'>You probably should as well</a>.</p>
    """
