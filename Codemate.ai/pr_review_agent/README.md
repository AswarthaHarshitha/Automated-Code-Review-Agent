# PR Review Agent

An AI-powered agent for reviewing pull requests across multiple git servers (GitHub, GitLab, Bitbucket). Written in Python, modular, and extensible.

## Features
- Fetches PR diffs from GitHub, GitLab, and Bitbucket
- Analyzes code changes for style, TODOs, and large functions (unique feature)
- Generates human-readable feedback and a quality score (unique feature)
- CLI interface for easy use

## Unique Features
- Detects large functions for refactoring suggestions
- Scores PRs based on detected issues

## Requirements
- Python 3.8+
- `requests`, `gitpython`

## Setup
1. Clone the repository or copy the codebase.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage (CLI)
Example for GitHub:
```bash
python main.py --provider github --repo https://github.com/owner/repo --pr 1 --token <your_github_token>
```

## Extending
- Add new providers by subclassing `BaseGitProvider` in `git_integration/`.
- Add new analysis rules in `code_analysis/analyzer.py`.

## Submission Checklist
- [x] Source code (excluding node_modules/venv)
- [x] Live working video
- [x] Live hosted URL (if web interface added)
- [x] GitHub repository link

## License
This project is original and plagiarism-free, created for the CodeMate Hackathon.
