#!/usr/bin/env python3

import unittest
from typing import Any, Dict, Tuple
from unittest import mock
from parameterized import parameterized
from unittest.mock import Mock, patch
from client import GithubOrgClient, get_json


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
            ("google"),
            ("abc"),    
        ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json: Mock) -> None: 
        """ Test that GithubOrgClient.org returns the correct value.
            and calls get_json exactly once.
            
        Args:
            org_name: The name of the Github organization to test
            mock_get_json: Mock object for the get_json function
        """
        expected_org: Dict = {"login": org_name,
                              "id": 123,
                              "repos_url": f"https://api.github.com/orgs/{org_name}/repos"
                            }
        mock_get_json.return_value = expected_org
        client: GithubOrgClient = GithubOrgClient(org_name)
        result: Dict = client.org
        self.assertEqual(result, expected_org)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/{org_name}")