# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:59:51 2022

@author: Okhrimchuk Roman & Maksym Veremchuk
for Sierentz Global Merchants


Test task
"""


class Solution:

    def longest_lucky_series(self, series):

        def check_lucky(rolling_series):
            # if all symbols are the same or at least one is less than 5.
            # as it is a dice, values can be in range from 1 to 6
            if len(set(rolling_series)) == 1 or any(i < '5' for i in rolling_series):
                return False
            return True

        res_string = ''

        for i in series:
            if check_lucky(i) and len(i) > len(res_string):
                res_string = i

        return res_string if res_string else 0
