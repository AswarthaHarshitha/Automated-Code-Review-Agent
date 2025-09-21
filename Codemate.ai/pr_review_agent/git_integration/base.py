"""
Base class for git server integration.
"""

from abc import ABC, abstractmethod

class BaseGitProvider(ABC):
    @abstractmethod
    def fetch_pr_diff(self, repo_url: str, pr_id: str) -> str:
        """
        Fetch the diff of a pull request from the git server.
        :param repo_url: Repository URL
        :param pr_id: Pull request ID or number
        :return: Diff as a string
        """
        pass
