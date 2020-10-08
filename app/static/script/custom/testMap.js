const recommenderFields = ["groups", "independence", "normality", "equal-variance"]
const testMap = [
    {
        "name": "t-test with one sample",
        "url": "./t-test-one-sample",
        "attributes": {
            "groups": ["1"],
            "independence": ["paired", "independent", "na"],
            "normality": ["yes"],
            "equal-variance": ["yes", "no", "na"]
        }
    },
    {
        "name": "t-test with two independent samples",
        "url": "./t-test-two-independent-samples",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["yes"],
            "equal-variance": ["yes"]
        }
    },
    {
        "name": "t-test with paired samples",
        "url": "./t-test-paired-samples",
        "attributes": {
            "groups": ["2"],
            "independence": ["paired"],
            "normality": ["yes"],
            "equal-variance": ["yes"]
        }
    },
    {
        "name": "t-test with two independent samples and unequal variance",
        "url": "./welches-t-test-two-independent-samples",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["yes"],
            "equal-variance": ["no"]
        }
    },
    {
        "name": "Bootstrap t-test with two independent samples",
        "url": "./bootstrap-t-test-two-independent-samples",
        "attributes": {
            "groups": ["2"],
            "independence": ["independent"],
            "normality": ["yes", "no"],
            "equal-variance": ["yes", "no"]
        }
    },
    {
        "name": "ANOVA – One way",
        "url": "./one-way-anova",
        "attributes": {
            "groups": ["3+"],
            "independence": ["independent"],
            "normality": ["yes"],
            "equal-variance": ["yes", "no"]
        }
    },
    {
        "name": "ANOVA – Two way",
        "url": "./one-way-anova",
        "attributes": {
            "groups": ["3+"],
            "independence": ["independent"],
            "normality": ["yes"],
            "equal-variance": ["yes", "no"]
        }
    }
]
