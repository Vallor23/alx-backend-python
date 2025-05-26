import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        # success cases
        ("single_level", {"a":1}, ["a"],1),
        ("single_level1", {"a": {"b": 1}}, ["a",], {"b": 1}),
        ("nested_level2", {"a": {"b": 1}}, ["a", "b"], 1),
        ("nested_level3", {"a": {"b": {"c": 1}}}, ["a", "b", "c"], 1),
        
    ])
    
    def test_access_nested_map(self, name, nested_map, path, expected):
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)
        
    @parameterized.expand([
        # edge cases
        ("missing_key", {"a":1}, ["a", "b"], KeyError ),
        ("non_mapping", {"a": {"b":1}}, ["a", "b", "c"], KeyError),
        ("empty_path", {"a":1}, [], KeyError),
    ])
    def test_access_nested_map_exceptions(self, name, nested_map, path, expected_exception):
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)