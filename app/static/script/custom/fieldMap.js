const fieldMap = {
    "alpha": {
            "label": "Significance Level (α):",
            "default": 0.05,
            "step": 0.01,
            "min": 0.01,
            "max": 0.2,
            "required": true
    },
    "power": {
            "label": "Statistical Power (1 - β):",
            "default": 0.8,
            "step": 0.01,
            "min": 0.5,
            "max": 1,
            "required": true
    },
    "effectSize": {
            "label": 'Effect Size (<a href="https://en.wikipedia.org/wiki/Effect_size#Cohen\'s_d" target="_blank">cohen\'s d</a>):',
            "default": 0.5,
            "step": "any",
            "required": false
    },
    "enrolmentRatio": {
            "label": 'Enrolment Ratio (n<sub>1</sub> / n<sub>2</sub>):',
            "default": 1,
            "step": "any",
            "min": 0,
            "required": true
    },
    "mean": {
            "label": 'Sample Mean:',
            "step": "any"
    },
    "stdDev": {
            "label": 'Standard Deviation:',
            "step": "any"
    },
    "n": {
            "label": 'Sample Size (n):',
            "step": 1,
            "min": 2
    }
}

const optionMap = {
    "sampleSize": {
        "generalFields": ["alpha", "power", "effectSize", "enrolmentRatio"],
        "sampleFields": ["mean", "stdDev"]
    },
    "power": {
        "generalFields": ["alpha", "effectSize"],
        "sampleFields": ["mean", "stdDev", "n"]
    },
    "pValue": {
        "generalFields": ["effectSize"],
        "sampleFields": ["mean", "stdDev", "n"]
    },
}
