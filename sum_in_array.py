# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:59:22 2022

@author: Okhrimchuk Roman & Maksym Veremchuk
for Sierentz Global Merchants


Test task
"""


class Solution:
    # Time Complexity: O(n^2)
    # Space : O(1)
    def brute_force_search(self, numbers, target):
        for i in range(len(numbers) - 1):
            for j in range(i + 1, len(numbers)):
                if numbers[i] + numbers[j] == target:
                    return numbers[i], numbers[j]
        return -1

    # Time Complexity: O(n)
    # Space : O(1)
    # this one is the most optimal algorithm by space and memory for sorted array
    def pointers_search(self, numbers, target):
        start, end = 0, len(numbers) - 1
        while start < end:
            current_sum = numbers[start] + numbers[end]
            if current_sum == target:
                return numbers[start], numbers[end]
            elif current_sum < target:
                start += 1
            else:
                end -= 1
        return -1

    # Time Complexity: O(n*log(n))
    # Space : O(1)
    def binary_search(self, numbers, target):
        i = 0
        while i < len(numbers):
            start, end = i, len(numbers) - 1
            while start <= end:
                middle = start + (end - start) // 2
                difference = target - numbers[start]
                if difference == numbers[middle]:
                    return numbers[start], numbers[middle]
                elif difference > middle:
                    start = middle + 1
                else:
                    end = middle - 1
        return -1

    # Time Complexity: O(n)
    # Space : O(n)
    def hashmap_search(self, numbers, target):

        values_dictionary = {}
        for number, value in enumerate(numbers):
            if target - value in values_dictionary.keys():
                return value, target - value
            else:
                values_dictionary[value] = number
        return -1
