#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)
        
    # @parameterized.expand([
    #     # edge cases
    #     ("missing_key", {"a":1}, ["a", "b"], KeyError ),
    #     ("non_mapping", {"a": {"b":1}}, ["a", "b", "c"], KeyError),
    #     ("empty_path", {"a":1}, (), KeyError),
    # ])
    # def test_access_nested_map_exceptions(self, name, nested_map, path, expected_exception):
    #     self.assertEqual(test_access_nested_map(nested_map, path), expected_exception)