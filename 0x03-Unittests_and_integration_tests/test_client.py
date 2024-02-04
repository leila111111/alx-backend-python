#!/usr/bin/env python3
"""github Client TEst.
"""
import unittest
from typing import Dict
from unittest.mock import PropertyMock, patch, Mock, MagicMock
from parameterized import parameterized, parameterized_class
from fixtures import TEST_PAYLOAD
from requests import HTTPError
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Testing GithubOrgClient"""
    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, response: Dict) -> None:
        """Testing org method."""
        github_client = GithubOrgClient(org)
        self.assertEqual(github_client.org(), response)
    