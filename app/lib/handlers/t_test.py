from app.lib.statistics.t_test import *
from app.lib.charts.t_test import *
from app.lib.formulae.t_test import *
from app.lib.notes.t_test import *
from app.lib import utils


def run_model(inputs):
    sample_fields = inputs['sampleFields']
    results = {"charts": {}}
    d = None

    # TARGET: SAMPLE SIZE
    if inputs['target'] == "sample-size":
        alpha = float(inputs['alpha'])
        power = float(inputs['power'])
        enrolment_ratio = float(inputs['enrolmentRatio'])

        # Stats and Formulas
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

        # Notes
        results['notes'] = generate_sample_size_notes(alpha, power)

        # Charts
        n_1 = results['statistics'][0]["two_sided_test"]
        n_2 = results['statistics'][1]["two_sided_test"]
        if d is None:
            d = utils.calculate_cohens_d(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2)
        results['charts']['chartOne'] = generate_power_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
        results['charts']['chartTwo'] = generate_effect_size_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
        results['charts']['chartThree'] = generate_distributions_chart_data(d=d, alpha=alpha, n_1=n_1, n_2=n_2)

    # TARGET: POWER
    elif inputs['target'] == "power":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])

        # Statistics and Formulas
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

        # Notes
        results['notes'] = generate_power_notes(alpha)

        # Charts
        power = results['statistics'][0]["two_sided_test"]
        if d is None:
            d = utils.calculate_cohens_d(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2)
        results['charts']['chartOne'] = generate_power_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=n_1/n_2)
        results['charts']['chartTwo'] = generate_effect_size_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=n_1/n_2)
        results['charts']['chartThree'] = generate_distributions_chart_data(d=d, alpha=alpha, n_1=n_1, n_2=n_2)

    # TARGET: MIN EFFECT SIZE
    elif inputs['target'] == "min-effect":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])
        power = float(inputs['power'])
        results['statistics'] = calculate_min_effect_size(n_1=n_1, n_2=n_2, alpha=alpha, power=power)
        results['formulae'] = create_min_effect_size_formula(n_1=n_1, n_2=n_2, alpha=alpha, power=power)
        results['notes'] = generate_min_effect_size_notes(alpha=alpha, power=power)

        # Charts
        d = results['statistics'][0]["two_sided_test"]
        results['charts']['chartOne'] = generate_power_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=n_1/n_2)
        results['charts']['chartTwo'] = generate_effect_size_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=n_1/n_2)
        results['charts']['chartThree'] = generate_distributions_chart_data(d=d, alpha=alpha, n_1=n_1, n_2=n_2)

    # TARGET: T-STATISTIC
    elif inputs['target'] == "t-stat":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])

        # Statistics
        if utils.all_sample_info_provided(sample_fields):
            x_bar_1 = float(sample_fields[0]['sampleMean'])
            s_1 = float(sample_fields[0]['sampleStdDev'])
            x_bar_2 = float(sample_fields[1]['sampleMean'])
            s_2 = float(sample_fields[1]['sampleStdDev'])
            d = utils.calculate_cohens_d(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2)
            t_stat = calculate_t_stat_from_means(x_bar_1=x_bar_1, s_1=s_1, n_1=n_1, x_bar_2=x_bar_2, s_2=s_2, n_2=n_2)
            results['formulae'] = create_t_stat_from_means_formula(x_bar_1=x_bar_1, s_1=s_1, n_1=n_1, x_bar_2=x_bar_2, s_2=s_2, n_2=n_2)
        else:
            d = float(inputs['effectSize'])
            x_bar_1, x_bar_2 = 1, 1 + d
            s_1, s_2 = 1, 1
            t_stat = calculate_t_stat_from_cohens_d(d=d, n_1=n_1, n_2=n_2)
            results['formulae'] = create_t_stat_from_d_formula(d=d, n_1=n_1, n_2=n_2)

        # Format Stats
        results['statistics'] = [{
            "label": "t-statistic",
            "one_sided_test": t_stat,
            "two_sided_test": t_stat
        }]

        # Notes
        results['notes'] = generate_t_stat_notes(n_1, n_2, d, t_stat)

        # Charts
        t_stat = results['statistics'][0]["two_sided_test"]
        results['charts']['chartOne'] = generate_t_distribution_chart_data(alpha=alpha, t_stat=t_stat, n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2)
        results['charts']['chartTwo'] = generate_t_statistic_vs_sample_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)
        results['charts']['chartThree'] = generate_t_statistic_vs_effect_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)

    # TARGET: P-VALUE
    elif inputs['target'] == "p-value":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])

        # Statistics
        if utils.all_sample_info_provided(sample_fields):
            x_bar_1 = float(sample_fields[0]['sampleMean'])
            s_1 = float(sample_fields[0]['sampleStdDev'])
            x_bar_2 = float(sample_fields[1]['sampleMean'])
            s_2 = float(sample_fields[1]['sampleStdDev'])
            d = utils.calculate_cohens_d(x_bar_1, s_1, n_1, x_bar_2, s_2, n_2)
            welches_df = utils.welches_degrees_of_freedom(s_1, n_1, s_2, n_2)
            t_stat = calculate_t_stat_from_means(x_bar_1=x_bar_1, s_1=s_1, n_1=n_1, x_bar_2=x_bar_2, s_2=s_2, n_2=n_2)
            results['statistics'] = calculate_p_value(t_stat=t_stat, df=welches_df)
            results['formulae'] = create_p_value_from_means_formula(x_bar_1=x_bar_1, s_1=s_1, n_1=n_1, x_bar_2=x_bar_2, s_2=s_2, n_2=n_2)
        else:
            d = float(inputs['effectSize'])
            x_bar_1, x_bar_2 = 1, 1 + d
            s_1, s_2 = 1, 1
            t_stat = calculate_t_stat_from_cohens_d(d=d, n_1=n_1, n_2=n_2)
            results['statistics'] = calculate_p_value(t_stat=t_stat, df=(n_1 + n_2 - 2))
            results['formulae'] = create_p_value_from_d_formula(d=d, n_1=n_1, n_2=n_2)

        # Notes
        results['notes'] = generate_p_value_notes(n_1=n_1,
                                                  n_2=n_2,
                                                  d=d,
                                                  p_one_sided=results['statistics'][0]['one_sided_test'],
                                                  p_two_sided=results['statistics'][0]['two_sided_test'],
                                                  t_stat=t_stat)

        # Charts
        results['charts']['chartOne'] = generate_t_distribution_chart_data(alpha=alpha, t_stat=t_stat, n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2)
        results['charts']['chartTwo'] = generate_p_value_vs_sample_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)
        results['charts']['chartThree'] = generate_p_value_vs_effect_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)

    return results
