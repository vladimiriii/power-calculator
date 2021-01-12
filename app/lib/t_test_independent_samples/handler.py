from app.lib.t_test_independent_samples.statistics import *
from app.lib.t_test_independent_samples.charts import *
from app.lib.t_test_independent_samples.formulae import *
from app.lib.t_test_independent_samples.notes import *
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
            mu_1 = 0
            mu_2 = mu_1 + d
            sigma_1, sigma_2 = 1, 1
            results['statistics'] = calculate_sample_size_from_cohens_d(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
            results['formulae'] = create_sample_size_from_d_formula(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)

        # Calculate vars
        n_1 = results['statistics'][0][1]
        n_2 = results['statistics'][1][1]
        if d is None:
            d = utils.calculate_cohens_d(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2)
        pooled_sd = utils.calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)

        # Notes
        results['notes'] = generate_sample_size_notes(alpha, power)
        results['chartText'] = generate_power_distributions_text(d=d, mu_1=mu_1, n_1=n_1, mu_2=mu_2, n_2=n_2, alpha=alpha, power=power)

        # Charts
        results['charts']['chartOne'] = generate_power_vs_sample_size_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
        results['charts']['chartTwo'] = generate_effect_size_vs_sample_size_chart_data(d=d, alpha=alpha, power=power, enrolment_ratio=enrolment_ratio)
        results['charts']['chartThree'] = generate_sampling_distributions_chart_data(mu_1=mu_1, mu_2=mu_2, sigma_1=sigma_1, sigma_2=sigma_2, n_1=n_1, n_2=n_2, alpha=alpha)

        # Labels
        results['labels'] = {
            "columns": ["", "One-sided test", "Two-sided test"],
            "rows": ["Sample 1 (n<sub>1</sub>)", "Sample 2 (n<sub>2</sub>)", "All Samples (n<sub>1</sub> + n<sub>2</sub>)"],
        }

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
            d = utils.calculate_cohens_d(mu_1, sigma_1, n_1, mu_2, sigma_2, n_2)
            results['statistics'] = calculate_power_from_means(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2, alpha=alpha)
            results['formulae'] = create_power_from_means_formula(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2, alpha=alpha)
        else:
            d = float(inputs['effectSize'])
            mu_1 = 0
            mu_2 = mu_1 + d
            sigma_1, sigma_2 = 1, 1
            results['statistics'] = calculate_power_from_cohens_d(d=d, n_1=n_1, n_2=n_2, alpha=alpha)
            results['formulae'] = create_power_from_d_formula(d=d, n_1=n_1, n_2=n_2, alpha=alpha)

        # Calculate vars
        power = results['statistics'][1][0]
        if d is None:
            d = utils.calculate_cohens_d(mu_1=mu_1, sigma_1=sigma_1, n_1=n_1, mu_2=mu_2, sigma_2=sigma_2, n_2=n_2)
        pooled_sd = utils.calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)

        # Notes
        welches_df = utils.welches_degrees_of_freedom(sigma_1, n_1, sigma_2, n_2)
        results['notes'] = generate_power_notes(alpha=alpha, df=welches_df)
        results['chartText'] = generate_power_distributions_text(d=d, mu_1=mu_1, n_1=n_1, mu_2=mu_2, n_2=n_2, alpha=alpha, power=power)

        # Charts
        results['charts']['chartOne'] = generate_sample_size_vs_power_chart_data(d=d, alpha=alpha, power=power, n_1=n_1, n_2=n_2)
        results['charts']['chartTwo'] = generate_effect_size_vs_power_chart_data(d=d, alpha=alpha, n_1=n_1, n_2=n_2)
        results['charts']['chartThree'] = generate_sampling_distributions_chart_data(mu_1=mu_1, mu_2=mu_2, sigma_1=sigma_1, sigma_2=sigma_2, n_1=n_1, n_2=n_2, alpha=alpha)

        # Labels
        results['labels'] = {
            "columns": ["Test type", "Statistical Power (1 - β)"],
            "rows": ["One-sided test", "Two-sided test"],
        }

    # TARGET: MIN EFFECT SIZE
    elif inputs['target'] == "min-effect":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])
        power = float(inputs['power'])
        results['statistics'] = calculate_min_effect_size(n_1=n_1, n_2=n_2, alpha=alpha, power=power)
        results['formulae'] = create_min_effect_size_formula(n_1=n_1, n_2=n_2, alpha=alpha, power=power)

        # Calculate Vars
        d = results['statistics'][1][0]
        mu_1 = 0
        mu_2 = mu_1 + d
        sigma_1, sigma_2 = 1, 1
        pooled_sd = utils.calculate_pooled_standard_deviation(n_1, n_2, sigma_1, sigma_2)

        # Notes
        welches_df = utils.welches_degrees_of_freedom(sigma_1, n_1, sigma_2, n_2)
        results['notes'] = generate_min_effect_size_notes(alpha=alpha, power=power, df=welches_df)
        results['chartText'] = generate_power_distributions_text(d=d, mu_1=mu_1, n_1=n_1, mu_2=mu_2, n_2=n_2, alpha=alpha, power=power)

        # Charts
        results['charts']['chartOne'] = generate_sample_size_vs_effect_size_data(d=d, alpha=alpha, power=power, n_1=n_1, n_2=n_2)
        results['charts']['chartTwo'] = generate_power_vs_effect_size_data(d=d, alpha=alpha, power=power, n_1=n_1, n_2=n_2)
        results['charts']['chartThree'] = generate_sampling_distributions_chart_data(mu_1=mu_1, mu_2=mu_2, sigma_1=sigma_1, sigma_2=sigma_2, n_1=n_1, n_2=n_2, alpha=alpha)

        # Labels
        results['labels'] = {
            "columns": ["Test type", "Minimum effect size"],
            "rows": ["One-sided test", "Two-sided test"],
        }

    # TARGET: T-STATISTIC
    elif inputs['target'] == "t-stat":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])

        # Statistics
        if utils.all_sample_info_provided(sample_fields):
            x_bar_1 = float(sample_fields[0]['mean'])
            s_1 = float(sample_fields[0]['stdDev'])
            x_bar_2 = float(sample_fields[1]['mean'])
            s_2 = float(sample_fields[1]['stdDev'])
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
        welches_df = utils.welches_degrees_of_freedom(s_1, n_1, s_2, n_2)
        t_critical_os = t.ppf(1 - alpha, df=welches_df)
        t_critical_ts = t.ppf(1 - alpha/2, df=welches_df)
        results['statistics'] = [
            [t_stat, t_critical_os],
            [t_stat, t_critical_ts],
        ]

        # Notes
        results['notes'] = generate_t_stat_notes(n_1, n_2, d, t_stat)
        results['chartText'] = generate_test_distribution_text(alpha=alpha, n_1=n_1, n_2=n_2, df=int(welches_df))

        # Charts
        t_stat = results['statistics'][0][0]
        results['charts']['chartOne'] = generate_t_statistic_vs_effect_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)
        results['charts']['chartTwo'] = generate_t_statistic_vs_sample_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)
        results['charts']['chartThree'] = generate_t_distribution_chart_data(alpha=alpha, t_stat=t_stat, n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2)

        # Labels
        results['labels'] = {
            "columns": ["Test Type", "t-statistic", 't-critical'],
            "rows": ["One-sided test", "Two-sided test"],
        }

    # TARGET: P-VALUE
    elif inputs['target'] == "p-value":
        n_1 = int(sample_fields[0]['n'])
        n_2 = int(sample_fields[1]['n'])
        alpha = float(inputs['alpha'])

        # Statistics
        if utils.all_sample_info_provided(sample_fields):
            x_bar_1 = float(sample_fields[0]['mean'])
            s_1 = float(sample_fields[0]['stdDev'])
            x_bar_2 = float(sample_fields[1]['mean'])
            s_2 = float(sample_fields[1]['stdDev'])
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
                                                  p_one_sided=results['statistics'][0][0],
                                                  p_two_sided=results['statistics'][1][0],
                                                  t_stat=t_stat)
        welches_df = utils.welches_degrees_of_freedom(s_1, n_1, s_2, n_2)
        results['chartText'] = generate_test_distribution_text(alpha=alpha, n_1=n_1, n_2=n_2, df=int(welches_df))

        # Charts
        results['charts']['chartOne'] = generate_p_value_vs_effect_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)
        results['charts']['chartTwo'] = generate_p_value_vs_sample_size_chart_data(n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2, alpha=alpha)
        results['charts']['chartThree'] = generate_t_distribution_chart_data(alpha=alpha, t_stat=t_stat, n_1=n_1, n_2=n_2, x_bar_1=x_bar_1, x_bar_2=x_bar_2, s_1=s_1, s_2=s_2)

        # Labels
        results['labels'] = {
            "columns": ["Test Type", "p-value"],
            "rows": ["One-sided test", "Two-sided test"],
        }

    return results
