#!/usr/bin/env python3
"""github Client TEst.
"""
import unittest
from typing import Dict
from unittest.mock import patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Testing GithubOrgClient returns the correct value
    """
    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch("client.get_json")
    def test_org(self, org: str, response: Dict) -> None:
        """Testing org method returns the correct value.
        """
        github_client = GithubOrgClient(org)
        self.assertEqual(github_client.org(), response)
