import pandas as pd
import random
import numpy as np
import datetime

import configurations
import constants

def get_sample_size(control_size, validation_size, rfm, log_type, ratio_list, main_ratio):
    control_size = int(control_size * main_ratio)
    validation_size = int(validation_size * main_ratio)
    s_s_cont = random.sample(ratio_list, 1)[0]
    s_s_valid = 1 - s_s_cont
    if log_type == 'login':
        if rfm.split('_')[2] in [1, 2]:
            s_s_valid = random.sample([0.45, 0.5, 0.55], 1)[0]
            s_s_cont = 1 - s_s_cont
    if log_type == 'baskets':
        if rfm.split('_')[2] == 1 and rfm.split('_')[1] in [1, 2]:
            s_s_valid = random.sample([0.4, 0.45, 0.5], 1)[0]
            s_s_cont = 1 - s_s_cont
    if log_type == 'order_screen':
        if rfm.split('_')[2] in [1, 2] and rfm.split('_')[1] in [1, 2]:
            s_s_valid = random.sample([0.5], 1)[0]
            s_s_cont = 1 - s_s_cont
    if log_type == 'order':
        if rfm.split('_')[2] == 1 and rfm.split('_')[1] == 1 and rfm.split('_')[3] in [1, 2, 3]:
            s_s_valid = random.sample([0.7, 0.8, 0.9], 1)[0]
            s_s_cont = 1 - s_s_cont

    print(int(control_size * s_s_cont), int(validation_size * s_s_valid))
    return int(control_size * s_s_cont), int(validation_size * s_s_valid)


def control_validation_rfm_segment_sampling(segment_dict, client_df, rfm, total_sample_size):
    _rfm_cont_vald = list(client_df.query("rfm == @rfm")['client_id'])
    sample_size = int(((segment_dict[rfm] * total_sample_size) / 2))
    print(sample_size, len(_rfm_cont_vald))
    if sample_size < len(_rfm_cont_vald):
        rfm_contol_sample = random.sample(_rfm_cont_vald, sample_size)
        rfm_validation_sample = list(set(_rfm_cont_vald) - set(rfm_contol_sample))
        if sample_size < len(rfm_validation_sample):
            rfm_validation_sample = random.sample(rfm_validation_sample, sample_size)
    else:
        rfm_contol_sample = random.sample(_rfm_cont_vald, int(len(_rfm_cont_vald) / 2))
        rfm_validation_sample = list(set(_rfm_cont_vald) - set(rfm_contol_sample))

    return rfm_contol_sample, rfm_validation_sample

def get_data_merged(rfm_contol_sample, rfm_validation_sample, control_login, valid_login,
                    control_basket, valid_basket, control_o_s, valid_o_s, control_o, valid_o, rfm):
    c_session = pd.DataFrame(rfm_contol_sample).rename(columns={0: 'client_id'})
    c_session['is_control'], c_session['session'] = 1, 1
    c_login = pd.DataFrame(control_login).rename(columns={0: 'client_id'})
    c_login['login'] = 1
    c_basket = pd.DataFrame(control_basket).rename(columns={0: 'client_id'})
    c_basket['basket'] = 1
    c_o_s = pd.DataFrame(control_o_s).rename(columns={0: 'client_id'})
    c_o_s['order_screen'] = 1
    c_o = pd.DataFrame(control_o).rename(columns={0: 'client_id'})
    c_o['ordered'] = 1

    v_session = pd.DataFrame(rfm_validation_sample).rename(columns={0: 'client_id'})
    v_session['is_control'], v_session['session'] = 0, 1
    v_login = pd.DataFrame(valid_login).rename(columns={0: 'client_id'})
    v_login['login'] = 1
    v_basket = pd.DataFrame(valid_basket).rename(columns={0: 'client_id'})
    v_basket['basket'] = 1
    v_o_s = pd.DataFrame(valid_o_s).rename(columns={0: 'client_id'})
    v_o_s['order_screen'] = 1
    v_o = pd.DataFrame(valid_o).rename(columns={0: 'client_id'})
    v_o['ordered'] = 1

    control_df = c_session
    if len(c_login) != 0:
        control_df = pd.merge(control_df, c_login, on='client_id', how='left')
    if len(c_basket) != 0:
        control_df = pd.merge(control_df, c_basket, on='client_id', how='left')
    if len(c_o_s) != 0:
        control_df = pd.merge(control_df, c_o_s, on='client_id', how='left')
    if len(c_o) != 0:
        control_df = pd.merge(control_df, c_o, on='client_id', how='left')
    for col in ['login', 'basket', 'order_screen', 'ordered']:
        if col not in list(control_df.columns):
            control_df[col] = None

    validation_df = v_session
    if len(v_login) != 0:
        validation_df = pd.merge(validation_df, v_login, on='client_id', how='left')
    if len(v_basket) != 0:
        validation_df = pd.merge(validation_df, v_basket, on='client_id', how='left')
    if len(v_o_s) != 0:
        validation_df = pd.merge(validation_df, v_o_s, on='client_id', how='left')
    if len(v_o) != 0:
        validation_df = pd.merge(validation_df, v_o, on='client_id', how='left')
    for col in ['login', 'basket', 'order_screen', 'ordered']:
        if col not in list(validation_df.columns):
            validation_df[col] = None

    output = pd.concat([control_df, validation_df])
    output['rfm'] = rfm
    return output

def get_ratio_list(lower_range, upper_range):
    ratio_list = []
    for r in range(0, 10000):
        ratio_list.append(np.random.random())
    return list(filter(lambda x: x < upper_range and x > lower_range, ratio_list))

def get_rfm_segmet_ratios(client_df):
    segment_dict = {}
    client_df['rfm'] = client_df.apply(lambda row:
                                       str(int(row['recency_segment'])) + '_' +
                                       str(int(row['frequency_segment'])) + '_' +
                                       str(int(row['monetary_segment'])) ,axis=1)

    segments_ratios_df = client_df.pivot_table(index='rfm',
                                               aggfunc={'client_id': 'count'}
                                               ).rename(columns={'client_id': 'count'}).reset_index()
    total_client_count = sum(list(segments_ratios_df['count']))
    segments_ratios_df['ratio'] = segments_ratios_df['count'] / total_client_count
    for rfm in list(segments_ratios_df['rfm'].unique()):
        segment_dict[rfm] = list(segments_ratios_df[segments_ratios_df['rfm'] == rfm]['ratio'])[0]
    return segment_dict, segments_ratios_df

def get_random_ab_test_generator(start_date, end_date, client_df, parameters):
    total_sessions = parameters['total_sessions']
    total_login = parameters['total_login']
    total_baskets = parameters['total_baskets']
    total_order_screen = parameters['total_order_screen']
    total_ordered = parameters['total_ordered']
    segment_dict, segments_ratios_df = get_rfm_segmet_ratios(client_df)
    ratio_list = get_ratio_list(constants.RANDOM_CLICK_RATIO_RANGES[0], constants.RANDOM_CLICK_RATIO_RANGES[1])
    final_df_2 = pd.DataFrame()
    while start_date < end_date:
        final_df = pd.DataFrame()
        for rfm in list(client_df['rfm'].unique()):
            print(rfm, len(client_df.query("rfm == @rfm")), segment_dict[rfm])
            _rfm_contol_sample, _rfm_validation_sample = control_validation_rfm_segment_sampling(segment_dict,
                                                                                                 client_df, rfm,
                                                                                                 total_sessions)
            # login
            _s_s_cont, _s_s_valid = get_sample_size(len(_rfm_contol_sample),
                                                    len(_rfm_validation_sample),
                                                    rfm, 'login', ratio_list, total_login / total_sessions)
            print(len(_rfm_contol_sample), _s_s_cont, len(_rfm_validation_sample), _s_s_valid)
            _control_login = random.sample(_rfm_contol_sample, _s_s_cont)
            _valid_login = random.sample(_rfm_validation_sample, _s_s_valid)
            # baskets
            _s_s_cont, _s_s_valid = get_sample_size(len(_control_login),
                                                    len(_valid_login),
                                                    rfm, 'baskets', ratio_list, total_baskets / total_login)
            print(len(_control_login), _s_s_cont, len(_valid_login), _s_s_valid)
            _control_basket = random.sample(_control_login, _s_s_cont)
            _valid_basket = random.sample(_valid_login, _s_s_valid)
            # order_screen
            _s_s_cont, _s_s_valid = get_sample_size(len(_control_basket),
                                                    len(_valid_basket),
                                                    rfm, 'order_screen', ratio_list, total_order_screen / total_baskets)
            print(len(_control_basket), _s_s_cont, len(_valid_basket), _s_s_valid)
            _control_o_s = random.sample(_control_basket, _s_s_cont)
            _valid_o_s = random.sample(_valid_basket, _s_s_valid)
            # order
            _s_s_cont, _s_s_valid = get_sample_size(len(_control_o_s),
                                                    len(_valid_o_s),
                                                    rfm, 'order', ratio_list, total_ordered / total_order_screen)
            print(len(_control_o_s), _s_s_cont, len(_valid_o_s), _s_s_valid)
            _control_o = random.sample(_control_o_s, _s_s_cont)
            _valid_o = random.sample(_valid_o_s, _s_s_valid)
            output_df = get_data_merged(_rfm_contol_sample, _rfm_validation_sample,
                                        _control_login, _valid_login,
                                        _control_basket, _valid_basket,
                                        _control_o_s, _valid_o_s,
                                        _control_o, _valid_o, rfm)
            final_df = output_df if len(final_df) == 0 else pd.concat([output_df, final_df])
        final_df['date'] = start_date
        final_df_2 = final_df if len(final_df_2) == 0 else pd.concat([final_df_2, final_df])
        start_date += datetime.timedelta(days=1)
    final_df_2 = random_data_generator_write_db(final_df_2, parameters)
    return final_df_2

def random_data_generator_write_db(final_df, parameters):
    final_df = final_df.reset_index(drop=True).reset_index().rename(columns={'index': 'session_id'})

    if parameters['is_randomly_generated_data_writing_db']:
        last_session = get_last_ab_test_session_id(parameters['days_test_starts'])
        final_df['session_id'] = final_df['session_id'] + last_session + 1
        final_df['session_id'] = final_df['session_id'].apply(lambda x: str(x) + '_id')
        final_df = final_df.fillna('-')
        insertDb = final_df.to_dict('results')
        cursor = configurations.connection_abtestdb.cursor()
        for row in insertDb:
            print(row)
            _query = "INSERT INTO designingtest "
            _i_col = constants.INSERT_COLUMNS
            _values = " VALUES ('{}', '{}', '{}', {}, {}, '{}'".format(row['session_id'], row['client_id'],
                                                                       str(row['date'])[0:10],
                                                                       row['is_control'], row['session'], row['rfm'])

            for col in constants.DB_INSERT_UPDATE:
                if row[col] != '-':
                    _i_col += ', ' + col
                    _values += ", " + str(int(row[col])) + " "
            _query = _query + _i_col + ')' + _values

            _query = _query + ')'
            cursor.execute(_query)
            configurations.connection_abtestdb.commit()
        cursor.close()
    if parameters['is_randomly_generated_data_writing_csv']:
        final_df.to_csv('ab_test.csv')
    return final_df

def get_last_ab_test_session_id(date):
    try:
        query = """
                SELECT
                    session_id        
                FROM designingtest WHERE date <= '{}'
        """.format(str(date)[0:10])
        df = pd.read_sql(query, configurations.connection_abtestdb)
        last_session = int(df.to_dict('resutls')[-1]['session_id'].split('_')[0])
    except:
        last_session = 0
    return last_session

