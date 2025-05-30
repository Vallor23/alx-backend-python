#!/usr/bin/env python3
"""Unit tests for utility functions in the utils module.

This module provides comprehensive test cases for the access_nested_map,
get_json,and memoize functions, ensuring they handle various inputs and
edge cases correctly as part of a GitHub organization client implementation.
"""

from typing import Any, Dict, Tuple
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: Dict,
                               path: Tuple, expected: Any) -> None:
        """Test access_nested_map returns expected value for valid paths."""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        # edge cases
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
        # ("empty_path", {"a":1}, (), KeyError),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Dict,
                                         path: Tuple) -> None:
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"test_payload": {"payload": True}}),
        ("http://holberton.io", {"test_payload": {"payload": False}})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url: str,
                      expected_json: Dict,
                      mock_requests_get: Mock) -> None:
        """Test that get_json returns the expected JSON from a URL."""
        mock_response = Mock()
        mock_response.json.return_value = expected_json
        mock_requests_get.return_value = mock_response
        actual_json = get_json(test_url)
        self.assertEqual(actual_json, expected_json)
        mock_requests_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        """Test that memoize caches the result of a method after one call.

        Args:
            return_value: The value to be returned by the mocked method.
            test_name: A descriptive name for the test case
            (used by parameterized).
        """
        class TestClass:
            """A test class with a memoized property."""

            def a_method(self) -> Any:
                return 42

            @memoize
            def a_property(self) -> Any:
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42
            test_instance = TestClass()

            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_a_method.assert_called_once()
