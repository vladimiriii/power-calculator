const recommenderFields = ["groups", "independence", "normality", "equal-variance"]
const testMap = [
    {
        "name": "z-test – One sample",
        "url": "./tests/z-test-one-sample",
        "status": "development",
        "attributes": {
            "groups": ["1"],
            "independence": ["na"],
            "normality": ["yes"],
            "known-variance": ["yes"]
        }
    },
    {
        "name": "z-test – Independent samples",
        "url": "./tests/z-test-independent-samples",
        "status": "development",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["yes"],
            "known-variance": ["yes"]
        }
    },
    {
        "name": "z-test – Paired samples",
        "url": "./tests/z-test-independent-samples",
        "status": "development",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["yes"],
            "known-variance": ["yes"]
        }
    },
    {
        "name": "t-test – One sample",
        "url": "./tests/t-test-one-sample",
        "status": "development",
        "attributes": {
            "groups": ["1"],
            "independence": ["paired", "independent", "na"],
            "normality": ["yes"],
            "known-variance": ["no"]
        }
    },
    {
        "name": "t-test – Independent samples",
        "url": "./tests/t-test-independent-samples",
        "status": "available",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["yes"],
            "known-variance": ["no"]
        }
    },
    {
        "name": "t-test – Paired samples",
        "url": "./tests/t-test-paired-samples",
        "status": "development",
        "attributes": {
            "groups": ["2"],
            "independence": ["paired"],
            "normality": ["yes"],
            "known-variance": ["no"]
        }
    },
    {
        "name": "ANOVA – One way",
        "url": "./tests/one-way-anova",
        "status": "development",
        "attributes": {
            "groups": ["3+"],
            "independence": ["independent"],
            "normality": ["yes"],
            "equal-variance": ["yes", "no"]
        }
    },
    {
        "name": "ANOVA – Two way",
        "url": "./tests/two-way-anova",
        "status": "development",
        "attributes": {
            "groups": ["3+"],
            "independence": ["independent"],
            "normality": ["yes"],
            "equal-variance": ["yes", "no"]
        }
    },
    {
        "name": "Chi-Squared χ<sup>2</sup> test",
        "url": "./tests/chi-squared",
        "status": "development",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["no"],
            "equal-variance": ["no"]
        }
    },
    {
        "name": "Mann-Whitney test",
        "url": "./tests/mann-whitney-test",
        "status": "development",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["no"],
            "known-variance": ["no"]
        }
    },
    {
        "name": "Wilcoxon Signed Rank test",
        "url": "./tests/wilcoxon-signed-rank-test",
        "status": "development",
        "attributes": {
            "groups": ["2"],
            "independence": ["paired"],
            "normality": ["no"],
            "equal-variance": ["no"]
        }
    },
    {
        "name": "Kruskal Wallis test",
        "url": "./tests/kruskal-wallis-test",
        "status": "development",
        "attributes": {
            "groups": ["3+"],
            "independence": ["independent"],
            "normality": ["no"],
            "equal-variance": ["no"]
        }
    }
]
