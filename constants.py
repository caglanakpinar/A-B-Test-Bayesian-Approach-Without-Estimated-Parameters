AB_TEST_DATAFRAME_KEY_COLUMS = ['day', 'is_control']
RANDOM_DATA_GENIRATOR = []
SEGMENT_DATA_COLUMN = ['rfm']
METRICS = ['login', 'basket', 'order_screen', 'ordered']
DB_INSERT_UPDATE = ['basket', 'login', 'ordered', 'order_screen']
INSERT_COLUMNS = " (session_id, client_id, date, is_control, session, rfm"
RANDOM_CLICK_RATIO_RANGES = [0.3, 0.8]

DEFAULT_RFM = ['1_1_4', '2_1_4', '2_1_3', '1_1_3', '2_1_2', '2_2_2', '2_2_3',
               '3_2_3', '3_2_2', '3_1_2', '3_3_2', '3_3_1', '3_2_1', '3_4_1',
               '3_4_2', '4_4_1', '3_1_3']