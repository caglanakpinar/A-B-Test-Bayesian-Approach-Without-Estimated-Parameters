import pandas as pd
import datetime

import constants
import configurations
import utils
from ab_test_generator import get_random_ab_test_generator


def data_gathering(parameters):
    start_date = datetime.datetime.strptime(parameters['days_test_starts'], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(parameters['days_test_starts'], '%Y-%m-%d')

    # check; where is the data?
    data_access_fail, ab_test_total, = 0, pd.DataFrame()
    try:
        if parameters['is_from_csv']:
            data_access_fail += 1
            control, validation = pd.read_csv('control.csv'), pd.read_csv('validation.csv')
            data_access_fail += 0.1
            control['is_control'], validation['is_control'] = 0, 1
            ab_test = pd.concat([control, validation])
            if not parameters['is_segmented']:
                data_access_fail += 0.1
                ab_test_total = ab_test[constants.AB_TEST_DATAFRAME_KEY_COLUMS + parameters.metrics]
            else:
                data_access_fail += 0.1
                ab_test_total = ab_test[constants.AB_TEST_DATAFRAME_KEY_COLUMS + parameters.metrics +
                                        constants.SEGMENT_DATA_COLUMN]

        else:
            data_access_fail = 2
            if parameters['is_from_db']:
                ab_test = get_data_from_db(start_date, end_date)
                if not parameters['is_segmented']:
                    data_access_fail += 0.1
                    ab_test_total = ab_test[constants.AB_TEST_DATAFRAME_KEY_COLUMS + parameters.metrics]
                else:
                    ab_test = get_segments(ab_test, start_date)
                    ab_test_total = ab_test[constants.AB_TEST_DATAFRAME_KEY_COLUMS + parameters.metrics +
                                            constants.SEGMENT_DATA_COLUMN]

            else:
                data_access_fail = 3
                if parameters['is_data_randomly_generated']:
                    segments = pd.read_csv('segments.csv')
                    ab_test_total = get_random_ab_test_generator(start_date, end_date, segments, parameters)
            data_access_fail += 1
    except:
        utils.error_print(data_access_fail, parameters)

    return ab_test_total



def get_data_from_db(start,end):
    # this the data set that I have created at my local postgresql. Query belongs to that db
    query = """
            SELECT
                client_id,
                is_control,
                date as day,
                sum(CASE WHEN session IS NOT NULL THEN 1 ELSE 0 END) as session_count,
                sum(CASE WHEN login IS NOT NULL THEN 1 ELSE 0 END) as login_count,
                sum(CASE WHEN basket IS NOT NULL THEN 1 ELSE 0 END) as basket_count,
                sum(CASE WHEN order_screen IS NOT NULL THEN 1 ELSE 0 END) as order_screen_count,
                sum(CASE WHEN ordered IS NOT NULL THEN 1 ELSE 0 END) as order_count

            FROM designingtest WHERE date >= '{}' and date <= '{}'
            GROUP BY client_id, is_control, date
    """.format(str(start)[0:10], str(end)[0:10])
    return pd.read_sql(query, configurations.connection_parameters['connection_abtestdb'])
    ab_test_total = pd.merge(ab_test_total, segments, on='client_id', how='left')

def get_segments(df, start_date):
    # this is also my local db. You need to update in order to connec to any db.
    query = """
            SELECT frequency_segment, monetary_segment, recency_segment, client_id
            FROM client_segments_daily WHERE date = '{}'
    """.format(str(start_date)[0:10])
    segments = pd.read_sql(query, configurations.connection_parameters['connection_clientsdb'])
    df = pd.merge(df, segments, on='client_id', how='left')
    df['rfm'] = df.apply(lambda row:
                         str(row['recency_segment']) + '_' +
                         str(row['frequency_segment']) + '_' + str(row['monetary_segment']), axis=1)
    return df

def writing_output(insert_db, insert_db_rfm, parameters):
    if parameters['is_there_any_prev_calcualtion_to_add_on']:
        pred_ab_test = pd.read_csv('daily_ab_test_results.csv')
        pd.concat([pred_ab_test, insert_db]).to_csv('daily_ab_test_results.csv')
        if parameters['is_segmented']:
            pred_ab_test_rfm = pd.read_csv('daily_ab_test_results_rfm.csv')
            pd.concat([pred_ab_test_rfm, insert_db_rfm]).to_csv('daily_ab_test_results_rfm.csv')






