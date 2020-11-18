from app.lib.statistics.t_test import *
from app.lib.charts.t_test import *
from app.lib.formulae.t_test import *
from app.lib.notes.t_test import *
from app.lib import utils


def run_model(inputs):
    sample_fields = inputs['sampleFields']
    results = {}

    # TARGET: SAMPLE SIZE
    if inputs['target'] == "sample-size":
        alpha = float(inputs['alpha'])
        power = float(inputs['power'])
        enrolment_ratio = float(inputs['enrolmentRatio'])
        if utils.all_sample_info_provided(sample_fields):
            mu_1 = float(sample_fields[0]['mean'])
            mu_2 = float(sample_fields[1]['mean'])
            sigma_1 = float(sample_fields[0]['stdDev'])
            sigma_2 = float(sample_fields[1]['stdDev'])
            results['statistics'] = calculate_sample_size_from_means(mu_1=mu_1, mu_2=mu_2, sigma_1=sigma_1, sigma_2=sigma_2, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
            results['formulae'] = create_sample_size_from_means_formula(mu_1=mu_1, mu_2=mu_2, sigma_1=sigma_1, sigma_2=sigma_2, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
        else:
            d = float(inputs['effectSize'])
            results['statistics'] = calculate_sample_size_from_cohens_d(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
            results['formulae'] = create_sample_size_from_d_formula(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
        results['notes'] = generate_sample_size_notes(alpha, power)

    # TARGET: POWER
    elif inputs['target'] == "power":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])
        if utils.all_sample_info_provided(sample_fields):
            mu_1 = float(sample_fields[0]['mean'])
            mu_2 = float(sample_fields[1]['mean'])
            sigma_1 = float(sample_fields[0]['stdDev'])
            sigma_2 = float(sample_fields[1]['stdDev'])
            results['statistics'] = calculate_power_from_means(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2, alpha=alpha)
            results['formulae'] = create_power_from_means_formula(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2, alpha=alpha)
        else:
            d = float(inputs['effectSize'])
            results['statistics'] = calculate_power_from_cohens_d(d=d, n_1=n_1, n_2=n_2, alpha=alpha)
            results['formulae'] = create_power_from_d_formula(d=d, n_1=n_1, n_2=n_2, alpha=alpha)
        results['notes'] = generate_power_notes(alpha)

    # TARGET: P-VALUE
    elif inputs['target'] == "p-value":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        if utils.all_sample_info_provided(sample_fields):
            mu_1 = float(sample_fields[0]['mean'])
            sigma_1 = float(sample_fields[0]['stdDev'])
            mu_2 = float(sample_fields[1]['mean'])
            sigma_2 = float(sample_fields[1]['stdDev'])
            results['statistics'] = caclulate_p_value_from_means(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2)
            results['formulae'] = create_p_value_from_means_formula(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2)
        else:
            d = float(inputs['effectSize'])
            results['statistics'] = caclulate_p_value_from_cohens_d(d=d, n_1=n_1, n_2=n_2)
            results['formulae'] = create_p_value_from_d_formula(d=d, n_1=n_1, n_2=n_2)
        results['notes'] = generate_p_value_notes(n_1, n_2)

    elif inputs['target'] == "min-effect":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])
        power = float(inputs['power'])
        results['statistics'] = caclulate_min_effect_size(n_1=n_1, n_2=n_2, alpha=alpha, power=power)
        results['formulae'] = create_min_effect_size_formula(n_1=n_1, n_2=n_2, alpha=alpha, power=power)
        results['notes'] = generate_min_effect_size_notes(alpha=alpha, power=power)
    results['charts'] = generate_chart_data(inputs, results['statistics'])

    return results
