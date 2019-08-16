import numpy as np
import pandas as pd
from math import sqrt
import random
from scipy.stats import beta
from scipy import stats
from scipy.stats import chi2, chi2_contingency
import constants



def calculate_t_test(p1, p2, click1, click2, n1, n2):
    p = (click1 + click2) / (n1 + n2)
    t = (p1 - p2) / sqrt(( p * (1 - p)) / ((1 / n1) + (1 / n2)) )
    df = n1 + n2 - 2
    pval = 1 - stats.t.sf(np.abs(t), df)*2  # two-sided pvalue = Prob(abs(t)>tt)
    confidence_limit = 1.96 * sqrt(((p1 * (1 - p1)) / n1) + ((p2 * (1 - p2)) / n2))
    confidence_intervals = [abs(p1 - p2) - confidence_limit, abs(p1 - p2) + confidence_limit]
    return pval, confidence_intervals

def chi_squared_test(total_control, click_control, total_validation, click_validation):
    observed_df = pd.DataFrame([
        {'test': 'control', 'click': click_control, 'non_click': total_control - click_control},
        {'test': 'validation', 'click': click_validation, 'non_click': total_control - click_validation},
        {'test': 'total', 'click': click_control + click_validation,
         'non_click': (total_control - click_control) + (total_control - click_validation)},
    ])
    observed_df['total'] = observed_df['click'] + observed_df['non_click']

    total = list(observed_df[observed_df['test'] == 'total']['total'])[0]

    x2_val = 0
    for g in ['control', 'validation']:
        for v in ['click', 'non_click']:
            _expected = (list(observed_df[observed_df['test'] == g]['total'])[0] *
                         list(observed_df[observed_df['test'] == 'total'][v])[0]) / total
            _observed = list(observed_df[observed_df['test'] == g][v])[0]

            # print(_expected, _observed, pow((_observed - _expected), 2) / _expected)
            x2_val += pow((_observed - _expected), 2) / _expected
    pval = chi2.cdf(x=x2_val, df=1)
    print(pval, "HO REJECTED!" if pval > 0.95 else "HO ACCEPTED!")
    return [pval, "HO REJECTED!" if pval > 0.95 else "HO ACCEPTED!"]

def get_metrics(df, metric, day, rfm):
    print("H0 : There is no difference on control and validation test sets on ", metric, " ratios.")
    print("p_control_", metric, " = ", "p_validation_", metric)
    print("H1: Thre statistically difference between Control And Validation sets ", metric, " ratios.")
    print("p_control_", metric, " != ", "p_validation_", metric)
    print(day)
    df_1 = df[df['day'] <= day]
    df_1 = df_1 if rfm is None else df_1[df_1['rfm'] == rfm]
    click1 =  sum(list(df_1[df_1['is_control'] == 0][metric]))
    click2 =  sum(list(df_1[df_1['is_control'] == 1][metric]))
    n1 = len(df_1[df_1['is_control'] == 0])
    n2 = len(df_1[df_1['is_control'] == 1])
    print(n1)
    return click1, click2, n1, n2, list(df_1[df_1['is_control'] == 0][metric]), list(df_1[df_1['is_control'] == 1][metric])

def definition_of_t_test(click1, click2, n1, n2):
    pval, confidence_intervals = calculate_t_test(click1 / n1, click2 / n2, click1, click2, n1, n2)
    print(1 - pval, click1 / n1, click2 / n2, "HO REJECTED!" if 1 - pval > 0.975 or 1 - pval < 0.25 else "HO ACCEPTED!")
    return [1 - pval, "HO REJECTED!" if 1 - pval > 0.975 or 1 - pval < 0.25 else "HO ACCEPTED!", confidence_intervals]

def bayesian_approach(c_val, v_val):

    x = np.linspace(0, 1, 200)
    a_control, b_control = 1, 1
    a_val, b_val = 1, 1
    number_of_sample = max(len(c_val), len(v_val))
    for ind in list(range(max(len(c_val), len(v_val)))):
        # control set a, b updating
        try:
            a_control += c_val[ind]  # click
            b_control += abs(c_val[ind] - 1)  # non-click
        except:
            if ind + 1 == len(c_val):
                print("out of index")

        # validation set a, b updating
        try:
            a_val += v_val[ind]  # click
            b_val += abs(v_val[ind] - 1)  # non-click
        except:
            if ind + 1 == len(v_val):
                print("out of index")

    control_p_values = stats.beta.rvs(a_control, b_control, size=len(c_val))
    validation_p_values = stats.beta.rvs(a_val, b_val, size=len(v_val))
    sample_size = min(len(control_p_values), len(validation_p_values))
    wins = validation_p_values[:sample_size] > control_p_values[:sample_size]
    print(np.mean(wins))
    return np.mean(wins)

def test_control_validation_sets(ab_test_total, metric, day, rfm):
    click_control, click_vald, n_control, n_vald, _control, _validation = get_metrics(ab_test_total, metric, day, None)
    print(click_control, click_vald, n_control, n_vald, day, metric)
    t_test_outputs = definition_of_t_test(click_control, click_vald, n_control, n_vald)
    print("chi squared check :")
    chi_squared_test_outputs = chi_squared_test(n_control, click_control, n_vald, click_vald)
    print("Bayesian approach :")
    wins = bayesian_approach(_control, _validation)
    print(str(round(wins, 3) * 100), " % times validation set of CTR is bigger than control set of CTR")

    return click_control / n_control, click_vald / n_vald, np.mean(wins) ,t_test_outputs, chi_squared_test_outputs

def test_data(ab_test_total, parameters):
    df_list = df_list_rfm = []
    if len(ab_test_total) != 0:
        days = list(ab_test_total['day'].unique())
        metrics = constants.METRICS if parameters['metrics'] == [] else parameters['metrics']
        if  len(set(metrics) - set(list(ab_test_total.columns))) == 0:
            for day in days:
                print(" day :", str(day)[0:10])
                for metric in metrics:
                    p_control, p_validation, win_ratio, t_test, chi_squared = test_control_validation_sets(ab_test_total, metric,
                                                                                                           day, None)
                    df_list.append({'p_control': p_control,
                                    'p_validation': p_validation,
                                    'win_ratio': win_ratio,
                                    't_test_p_value': t_test[0],
                                    't_test_H0': t_test[1],
                                    't_test_left_tail': t_test[2][0],
                                    't_test_right_tail': t_test[2][1],
                                    'chi_squared_p_value': chi_squared[0],
                                    'chi_squared_H0': chi_squared[1],
                                    'bayesian_approach_confidence': win_ratio,
                                    'day': day,
                                    'metrics': metric
                                    })
                    if parameters['is_segmented']:
                        if day == days[0]:
                            rfm_segments = list(ab_test_total['rfm'].unique())
                        for rfm in rfm_segments:
                            print("rfm segment :", rfm)
                            p_control, p_validation, win_ratio, t_test, chi_squared = test_control_validation_sets(ab_test_total,
                                                                                                                   metric, day,
                                                                                                               rfm)

                            df_list_rfm.append({'p_control': p_control,
                                                'p_validation': p_validation,
                                                'win_ratio': win_ratio,
                                                't_test_p_value': t_test[0],
                                                't_test_H0': t_test[1],
                                                't_test_left_tail': t_test[2][0],
                                                't_test_right_tail': t_test[2][1],
                                                'chi_squared_p_value': chi_squared[0],
                                                'chi_squared_H0': chi_squared[1],
                                                'bayesian_approach_confidence': win_ratio,
                                                'rfm': rfm,
                                                'day': day,
                                                'metrics': metric
                                                })
        else:
            print("make sure all metrics are assigned to data")
            print("Here are not assigned columns :")
            print(list(set(metrics) - set(list(ab_test_total.columns))))
    return pd.DataFrame(df_list), pd.DataFrame(df_list_rfm)