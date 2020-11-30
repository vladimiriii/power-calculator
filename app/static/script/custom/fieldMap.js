const fieldMap = {
    "alpha": {
            "label": "Significance Level (α):",
            "default": 0.05,
            "step": 0.005,
            "min": 0.01,
            "max": 0.2,
            "required": true
    },
    "power": {
            "label": "Statistical Power (1 - β):",
            "default": 0.8,
            "step": 0.005,
            "min": 0.5,
            "max": 1,
            "required": true
    },
    "effectSize": {
            "label": 'Effect Size (<a href="https://en.wikipedia.org/wiki/Effect_size#Cohen\'s_d" target="_blank">Cohen\'s d</a>):',
            "default": 0.5,
            "step": "any",
            "required": false
    },
    "enrolmentRatio": {
            "label": 'Ratio of observations (n<sub>1</sub> / n<sub>2</sub>):',
            "default": 1,
            "step": "any",
            "min": 0,
            "required": true
    },
    "mean": {
            "label": 'Mean: ',
            "step": "any"
    },
    "stdDev": {
            "label": 'Standard Deviation: ',
            "step": "any"
    },
    "sampleMean": {
            "label": "Sample Mean: ",
            "step": "any"
    },
    "sampleStdDev": {
            "label": "Sample Standard Deviation: ",
            "step": "any"
    },
    "n": {
            "label": "Sample Size (n): ",
            "step": 1,
            "min": 2
    }
}

const optionMap = {
    "planning": {
        "sample-size": {
            "displayName": "Minimum Sample Size",
            "compulsoryFields": {
                "oneOf": ["alpha", "power", "enrolmentRatio"],
                "perGroup": []
            },
            "orFields": {
                "oneOf": ["effectSize"],
                "perGroup": ["mean", "stdDev"]
            }
        },
        "power": {
            "displayName": "Statistical Power",
            "compulsoryFields": {
                "oneOf": ["alpha"],
                "perGroup": ["n"]
            },
            "orFields": {
                "oneOf": ["effectSize"],
                "perGroup": ["mean", "stdDev"]
            }
        },
        "min-effect": {
            "displayName": "Minimum Effect Size",
            "compulsoryFields": {
                "oneOf": ['alpha', 'power'],
                "perGroup": ["n"]
            },
            "orFields": {
                "oneOf": [],
                "perGroup": []
            }
        }
    },
    "assessing": {
        "t-stat": {
            "displayName": "t-statistic",
            "compulsoryFields": {
                "oneOf": ['alpha'],
                "perGroup": ["n"]
            },
            "orFields": {
                "oneOf": ["effectSize"],
                "perGroup": ["sampleMean", "sampleStdDev"]
            }
        },
        "p-value": {
            "displayName": "p-value",
            "compulsoryFields": {
                "oneOf": ['alpha'],
                "perGroup": ["n"]
            },
            "orFields": {
                "oneOf": ["effectSize"],
                "perGroup": ["sampleMean", "sampleStdDev"]
            }
        }
    }
}
