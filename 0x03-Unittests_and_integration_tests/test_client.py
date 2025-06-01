#!/usr/bin/env python3

import unittest
from typing import Any, Dict, List, Tuple
from unittest import mock
from parameterized import parameterized
from unittest.mock import Mock, patch
from client import GithubOrgClient, get_json
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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
        expected_org: Dict = {
            "login": org_name,
            "id": 123,
            "repos_url": "https://api.github.com/orgs/{org_name}/repos"
        }
        mock_get_json.return_value = expected_org
        client: GithubOrgClient = GithubOrgClient(org_name)
        result: Dict = client.org
        self.assertEqual(result, expected_org)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json: Mock):
        """Test that GithubOrgClient._public_repos_url returns the correct URL.

        Args:
         mock_get_json: Mock object for the get_json function.
        """
        org_name: str = "test_org"
        repos_url: str = "https://api.github.com/orgs/test_org/repos"
        mock_get_json.return_value = {"repos_url": repos_url}
        client: GithubOrgClient = GithubOrgClient(org_name)
        result = client._public_repos_url
        self.assertEqual(result, repos_url)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test_org/repos")
        
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json: Mock,) -> None:
        """Test that GithubOrgClient.public_repos returns the correct list of repo names.

        Args:
            mock_get_json: Mock object for the get_json function.
        """
        org_name: str = "test_org"
        repos_url: str = "https://api.github.com/orgs/test_org/repos"
        repos_payload: List[Dict] = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}}
        ]
        mock_get_json.side_effect = repos_payload

        with patch.o('client.GithubOrgClient._public_repos_url', return_value=repos_url) as mock_repos_url:
            client: GithubOrgClient = GithubOrgClient(org_name)
            result: List[str] = client.public_repos()
            result_mit: List[str] = client.public_repos(license = "mit")

            self.assertEqual(result, ["repo1", "repo2"])
            self.assertEqual(result_mit, ["repo1"])

            mock_get_json.assert_called_once_with(repos_url)
            mock_repos_url.assert_called_once()
            _ = client.public_repos()
            mock_get_json.assert_called_once_with(repos_url)
            
    @parameterized.expand([
        ({"license": {"key": "mit"}, "name": "repo1"}, "mit", True),
        ({"license": {"key": "apache-2.0"}, "name": "repo1"}, "mit", False),
        ({"license": None, "name": "repo1"}, "mit", False),
        ({}, "mit", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str, expected: bool) -> None:
        """Test that GithubOrgClient.has_license correctly checks repo licenses."""
        result: bool = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up class by mocking requests.get with fixture payloads"""
        def get_json_side_effect(url):
            """Side effect for requests.get().json() based on URL"""
            mock_response = Mock()
            if url == "https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload.get("repos_url"):
                mock_response.json.return_value = cls.repos_payload
            return mock_response

        cls.get_patcher = patch('requests.get', side_effect=get_json_side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher for requests.get"""
        cls.get_patcher.stop()