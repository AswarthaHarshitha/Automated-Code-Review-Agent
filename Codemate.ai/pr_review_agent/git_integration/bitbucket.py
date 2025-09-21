"""
Bitbucket integration for PR Review Agent
"""

import requests
from .base import BaseGitProvider

class BitbucketProvider(BaseGitProvider):
    def __init__(self, username: str, app_password: str, api_url: str = "https://api.bitbucket.org/2.0"):
        self.username = username
        self.app_password = app_password
        self.api_url = api_url

    def fetch_pr_diff(self, repo_url: str, pr_id: str) -> str:
        # Extract workspace and repo_slug from URL
        parts = repo_url.rstrip('/').split('/')
        workspace, repo_slug = parts[-2], parts[-1]
        url = f"{self.api_url}/repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/diff"
        response = requests.get(url, auth=(self.username, self.app_password))
        response.raise_for_status()
        return response.text
