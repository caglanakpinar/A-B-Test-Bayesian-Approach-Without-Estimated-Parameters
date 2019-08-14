import datetime
import data_access
import configurations
import ab_testing


parameters = {
    'days_test_starts': '2019-08-05',  # day it started, must be string at first
    'days_test_ends': '2019-08-25', # not included
    'total_sessions': 18000, # for randomly generating data
    'total_login': 14000, # for randomly generating data
    'total_baskets': 10000, # for randomly generating data
    'total_order_screen': 9000, # for randomly generating data
    'total_ordered': 8000, # for randomly generating data
    'is_from_db': True,
    'db_connection_values': configurations.connection_parameters,
    'is_data_randomly_generated': False, # if there is no data for run the a_b test
    'is_randomly_generated_data_writing_db': True, # if you want to write ramdom ab test output into a db of table
    'is_randomly_generated_data_writing_csv': True, # if you want to write ramdom ab test output into a csv
    'is_from_csv': False,  # if there is data that you want tu run
     # make sure control.csv, validation.csv are included to project, make sure same directory as project
     # columns are belongs; day, metrics (write metrics for calculating Conversion rate)
     # each metrics must include 0 and 1. For instance check sample data set belongs to project or randomly generated data set
    'metrics': [], # which metrics do you want to check on for Conversion Rate. You may write more than one
    'is_segmented': True, # if every each transaction of client are segmented into the groups
    # if this statement is true make sure that you have rfm columns in csv files or connect connection_clientsdb for segments
    # I have done RFM segmentation at this point, which I am familiar with the assumpions of it.
    'segment_Data_column': 'rfm' # pls assign rfm to if there is segmented data column, otherwise keep it None
}

def main(parameters):
    ab_test_total = data_access.data_gathering(parameters)
    daily_ab_test_results, daily_ab_test_results_segmented = ab_testing.test_data(ab_test_total, parameters)
    

if __name__ == '__main__':
  main(parameters)