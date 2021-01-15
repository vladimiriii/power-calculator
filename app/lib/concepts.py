concept_map = {
    "t-test-independent-samples": [
        "alpha",
        "power",
        "d"
    ]
}


concepts_text = {
    "alpha": """<p><strong>Significance Level (α)</strong>: The probability of incorrectly rejecting the null hypothesis (H<sub>0</sub>: θ = 0; where θ = μ<sub>1</sub> - μ<sub>2</sub>), also known as the false positive rate or the Type I error rate. An α of 0.05 (5%) means that if we repeated an experiment where we drew samples from the same population many times, we would expect to incorrectly reject the null hypothesis in 5% of cases. α can also be thought of as a measure of how extreme the observed difference in sample means has to be before we reject the null hypothesis. With an α of 0.05, we would reject the null hypothesis when observing a difference that we would expect to see 5% (or less) of the time when drawing two samples from the same population.</p>""",
    "power": """<p><strong>Statistical Power (1 - β)</strong>: β is the probability that we will fail to reject the null hypothesis when the samples are drawn from different populations. This is also known as the false negative rate or the Type II error rate. Statistical power or 1 - β is therefore the probablity that we will correctly reject the null hypothesis. In the same way that we can draw samples with different means from the same population, there is also a risk that we draw samples with very similar means from two different populations.</p>""",
    "d": """<p><strong>Effect Size (Cohen's d)</strong>: A standardized measure of the difference in the means (can be sample or population means depending on the context). The difference in means is divided by the <a href="https://en.wikipedia.org/wiki/Pooled_variance" target="_blank">pooled standard deviation</a> of the two samples/populations to provide a metric, in units of standard deviations, that can be compared across studies. It can also be used directly in some calculations instead of the means and standard deviations of the samples.</p>"""
}
