import pandas as pd
import random
import numpy as np

class random_transaction_generator:
    def __init__(self, segments, parameters, metrics):
        self.parameters = parameters
        self.metrics = metrics
        self.segments = segments
        self.rfm_list = list(segments['rfm'].unique())

        self.segment_ratios = segments.pivot_table(index='rfm',
                                                   aggfunc={'client_id': 'count'}
                                                   ).reset_index().rename(columns={'client_id': 'ratio'})
        self.total_client_count = sum(self.segment_ratios['ratio'])
        self.segment_ratios['ratio'] = self.segment_ratios['ratio'] / self.total_client_count
        self.segment_dict = {}
        for rfm in list(self.segments['rfm'].unique()):
            self.segment_dict[rfm] = list(segments[segments['rfm'] == rfm]['ratio'])[0]

        self.rfm = None
        self.rfm_control_sample = []
        self.rfm_validation_sample = []
        self.main_ratio = None
        self.log_type = 'login'
        self.ratio_list = []
        self.sample_size_control =  None
        self.sample_size_validation = None
        self.metrics

    def control_validation_rfm_segment_sampling(self):
        _rfm_cont_vald = list(self.segments.query("rfm == @rfm")['client_id'])
        sample_size = int(((self.segment_dict[self.rfm] * self.parameters.total_sample_size) / 2))
        if sample_size < len(_rfm_cont_vald):
            self.rfm_control_sample = random.sample(_rfm_cont_vald, sample_size)
            self.rfm_validation_sample = list(set(_rfm_cont_vald) - set(self.rfm_control_sample))
            if sample_size < len(self.rfm_validation_sample):
                rfm_validation_sample = random.sample(self.rfm_validation_sample, sample_size)
        else:
            self.rfm_control_sample = random.sample(_rfm_cont_vald, int(len(_rfm_cont_vald) / 2))
            self.rfm_validation_sample = list(set(_rfm_cont_vald) - set(self.rfm_control_sample))

    def get_main_ratio(self):
        if self.log_type == 'login':
            self.main_ratio =  self.parameters.total_login / self.parameters.total_sessions
        if self.log_type == 'baskets':
            self.main_ratio =  self.parameters.total_baskets / self.parameters.total_login
        if self.log_type == 'order_screen':
            self.main_ratio =  self.parameters.order_screen / self.parameters.total_baskets
        if self.log_type == 'login':
            self.main_ratio =  self.parameters.total_ordered / self.parameters.order_screen

    def get_ratio_list(self):
        for r in range(0, 10000):
            self.ratio_list.append(np.random.random())
        self.ratio_list = list(filter(lambda x: x < 0.8 and x > 0.3, self.ratio_list))

    def get_sample_size(self):

        self.get_main_ratio()
        self.get_ratio_list()
        control_size = int(self.rfm_control_sample * self.main_ratio)
        validation_size = int(self.rfm_validation_sample * self.main_ratio)
        s_s_cont = random.sample(self.ratio_list, 1)[0]
        s_s_valid = 1 - s_s_cont
        if self.log_type == 'login':
            if self.rfm.split('_')[2] in [1, 2]:
                s_s_valid = random.sample([0.45, 0.5, 0.55], 1)[0]
                s_s_cont = 1 - s_s_cont
        if self.log_type == 'baskets':
            if self.rfm.split('_')[2] == 1 and self.rfm.split('_')[1] in [1, 2]:
                s_s_valid = random.sample([0.4, 0.45, 0.5], 1)[0]
                s_s_cont = 1 - s_s_cont
        if self.log_type == 'order_screen':
            if self.rfm.split('_')[2] in [1, 2] and self.rfm.split('_')[1] in [1, 2]:
                s_s_valid = random.sample([0.5], 1)[0]
                s_s_cont = 1 - s_s_cont
        if self.log_type == 'order':
            if self.rfm.split('_')[2] == 1 and self.rfm.split('_')[1] == 1 and self.rfm.split('_')[3] in [1, 2, 3]:
                s_s_valid = random.sample([0.7, 0.8, 0.9], 1)[0]
                s_s_cont = 1 - s_s_cont
        self.sample_size_control = self.rfm_control_sample * s_s_cont
        self.sample_size_validation = self.rfm_validation_sample * s_s_valid
