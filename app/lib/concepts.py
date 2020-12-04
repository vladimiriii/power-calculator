concept_map = {
    "t-test-independent-samples": [
        "alpha",
        "power",
        "d"
    ]
}


concepts_text = {
    "alpha": """<p><strong>Significance Level (α)</strong>: The probability of incorrectly rejecting the null hypothesis (H<sub>0</sub>: θ = 0; where θ = μ<sub>1</sub> - μ<sub>2</sub>), also know as the false positive or Type I error rate. An α of 0.05 (5%) means we expect to reject the null hypothesis in 5% of studies where the null hypothesis is true. α can also be thought of as a measure of how extreme the observed difference in sample means has to be before we reject the null hypothesis, with an α of 0.05 meaning we would reject the null hyupothesis when observing a difference that we would expect to see 5% (or less) of the time when drawing two samples from the same population.</p>""",
    "power": """<p><strong>Statistical Power (1 - β)</strong>: β is the probability that we will fail to reject the null hypothesis when there is an underlying difference (the false negative or Type II error rate). Statistical power or 1 - β is therefore the probablity that we will correctly reject the null hypothesis. In the same way that we could draw samples with different means when there is no real difference, there is also a risk that we draw samples with very similar means from two very different populations.</p>""",
    "d": """<p><strong>Effect Size (Cohen's d)</strong>: A standardized measure of the difference in the means (can be sample or population means depending on the context). The difference in means is divided by the <a href="https://en.wikipedia.org/wiki/Pooled_variance" target="_blank">pooled standard deviation</a> of the two samples/populations to provide a metric (in standard deviations) that can be compared across studies.</p>"""
}
