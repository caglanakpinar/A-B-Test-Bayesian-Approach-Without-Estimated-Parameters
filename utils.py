def error_print(data_access_fail, parameters):
    if data_access_fail == 1:
        print("You are collecting data from .csv. Make sure to update is_from_csv parameter.")
        print("make sure control.csv and validation.csv are in the same directory")
    if data_access_fail == 1.1:
        print("make sure control.csv and validation.csv has same data_sets")
    if data_access_fail == 1.2:
        if parameters.metrics == []:
            print("pls guide, what metrics of conversion rate will be tested?")
        else:
            print("pls make sure that data has column of 'day' ")
            print("pls make sure every metric has value of 0 ,1")
        if parameters['is_segmented']:
            print("pls make sure you have rfm column at data sets")
    if data_access_fail == 2:
        print("You are collecting data from DB connection. Make sure to update is_from_db parameter.")
        print("check your connections")
    if data_access_fail == 2.1:
        if parameters.metrics == []:
            print("pls guide, what metrics of conversion rate will be tested?")
        else:
            print("pls make sure that data has column of 'day' ")
            print("pls make sure every metric has value of 0 ,1")
        if parameters['is_segmented']:
            print("pls make sure you have rfm column at data sets")