"""
GitHub integration for PR Review Agent
"""

import requests
from .base import BaseGitProvider

class GitHubProvider(BaseGitProvider):
    def __init__(self, token: str):
        self.token = token
        self.api_url = "https://api.github.com"

    def fetch_pr_diff(self, repo_url: str, pr_id: str) -> str:
        # Extract owner and repo from URL
        parts = repo_url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3.diff"
        }
        url = f"{self.api_url}/repos/{owner}/{repo}/pulls/{pr_id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text

    def fetch_pr_stats(self, repo_url: str, pr_id: str) -> dict:
        """Fetch PR summary: files changed, additions, deletions, contributors."""
        parts = repo_url.rstrip('/').split('/')
        owner, repo = parts[-2], parts[-1]
        headers = {"Authorization": f"token {self.token}"}
        url = f"{self.api_url}/repos/{owner}/{repo}/pulls/{pr_id}"
        pr_resp = requests.get(url, headers=headers)
        pr_resp.raise_for_status()
        pr_data = pr_resp.json()
        files_url = pr_data.get('url') + '/files'
        files_resp = requests.get(files_url, headers=headers)
        files_resp.raise_for_status()
        files_data = files_resp.json()
        contributors = set()
        for f in files_data:
            if 'patch' in f:
                for line in f['patch'].split('\n'):
                    if line.startswith('+') or line.startswith('-'):
                        contributors.add(pr_data['user']['login'])
        return {
            'files_changed': pr_data.get('changed_files'),
            'additions': pr_data.get('additions'),
            'deletions': pr_data.get('deletions'),
            'contributors': list(contributors)
        }
