#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map,get_json, memoize
from unittest.mock import patch, Mock
class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)
        
    @parameterized.expand([
        # edge cases
        ({}, ["a",]),
        ({"a": 1}, ["a", "b"]),
        # ("empty_path", {"a":1}, (), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)
            
class TestGetJson(unittest.TestCase):
    
    @parameterized.expand([
        ("http://example.com",{"test_payload": {"payload": True}}),
        ("http://holberton.io",{"test_payload": {"payload": False}})
    ])
    
    @patch('requests.get') 
    def test_get_json(self, test_url, expected_json, mock_requests_get):
        mock_response = Mock() # creates a mock object to simulate the response from requests.get -> mock_requests_get(url)
        mock_response.json.return_value = expected_json # sets the mock’s json() method to return the expected JSON.
        mock_requests_get.return_value = mock_response # configures mock_requests_get to return mock_response
        actual_json = get_json(test_url)
        self.assertEqual(actual_json, expected_json)
        mock_requests_get.assert_called_once_with(test_url)

class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42
            
            @memoize
            def a_property(self):
                return self.a_method()
        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42
            test_instance = TestClass()
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()