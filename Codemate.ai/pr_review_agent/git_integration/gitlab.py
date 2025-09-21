"""
GitLab integration for PR Review Agent
"""

import requests
from .base import BaseGitProvider

class GitLabProvider(BaseGitProvider):
    def __init__(self, token: str, api_url: str = "https://gitlab.com/api/v4"):
        self.token = token
        self.api_url = api_url

    def fetch_pr_diff(self, repo_url: str, pr_id: str) -> str:
        # Extract namespace/project from URL
        parts = repo_url.rstrip('/').split('/')
        namespace = '/'.join(parts[-2:])
        headers = {
            "PRIVATE-TOKEN": self.token
        }
        url = f"{self.api_url}/projects/{namespace.replace('/', '%2F')}/merge_requests/{pr_id}/changes"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
