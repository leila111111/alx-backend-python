#!/usr/bin/env python3
"""github Client TEst.
"""
from parameterized import parameterized, parameterized_class
import unittest
from typing import Dict
from unittest.mock import PropertyMock, patch, Mock, MagicMock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """Testing GithubOrgClient returns the correct value
    """
    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, response: Dict, mock_test) -> None:
        """Testing org method returns the correct value.
        """
        mock_test.return_value = response
        github_client = GithubOrgClient(org)
        self.assertEqual(github_client.org, response)

    def test_public_repos_url(self) -> None:
        """unit-test GithubOrgClient._public_repos_url
        """
        name = "google"
        test_payload = {"repos_url": "http://google.com"}
        with patch('client.GithubOrgClient.org',
                   PropertyMock(return_value=test_payload)):
            github_org_client = GithubOrgClient(name)
            self.assertEqual(github_org_client._public_repos_url,
                             "http://google.com")

    @patch('client.get_json')
    def test_public_repos(self, json_mock: MagicMock) -> None:
        """unit-test GithubOrgClient._public_repos_url
        """
        names = [{"name": "name1", "license": {"key": "license1"}},
                 {"name": "name2", "license": {"key": "license2"}},
                 {"name": "name3"}]
        json_mock.return_value = names
        with mock.patch('client.GithubOrgClient._public_repos_url',
                        PropertyMock(return_value="www.vue.com")):
            github_org_client = GithubOrgClient("google")
            self.assertEqual(github_org_client.public_repos(),
                             ["name1", "name2", "name3"])
            self.assertEqual(github_org_client.public_repos("license1"),
                             ["name1"])
            self.assertEqual(github_org_client.public_repos("license2"),
                             ["name2"])
            self.assertEqual(github_org_client.public_repos("license3"),
                             [])
        json_mock.assert_called_once_with("www.vue.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict,
                         licence: str, expect: bool) -> None:
        """Testing has_license"""
        objet = GithubOrgClient("google")
        client_lisence = objet.has_license(repo, licence)
        self.assertEqual(client_lisence, expect)


@parameterized_class(
    [
        {
            'org_payload': TEST_PAYLOAD[0][0],
            'repos_payload': TEST_PAYLOAD[0][1],
            'expected_repos': TEST_PAYLOAD[0][2],
            'apache2_repos': TEST_PAYLOAD[0][3],
        },
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Testing IntegrationGithubOrgClient"""
    @classmethod
    def setUpClass(cls) -> None:
        """Setclass.
        """
        repo_rout = {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
        }

        def get_payload(url):
            if url in repo_rout:
                rout = Mock()
                rout.json.return_value = repo_rout[url]
                return rout
            return HTTPError
        cls.get_patcher = patch('requests.get', side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Testing public_repos method"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Testing public_repos_with_license method"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """class of tear down"""
        cls.get_patcher.stop()
