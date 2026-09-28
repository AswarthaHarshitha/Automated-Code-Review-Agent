# Automated Code Review Agent

A command-line agent that reviews pull requests on GitHub, GitLab and Bitbucket. It fetches the PR diff, runs static analysis (lint, security and complexity) on the changed Python code, asks a locally hosted LLM for review comments, scores the PR and exports the review as Markdown and PDF. Built for the CodeMate hackathon.

## Features

- **Multi-provider** — GitHub (REST API, including PR stats: files changed, additions, deletions, contributors), GitLab and Bitbucket, behind a common `BaseGitProvider` interface.
- **Syntax-highlighted diff** in the terminal via Rich.
- **Static analysis of added Python code** — `pylint` (errors, warnings, conventions, refactors), `bandit` (security) and `radon` (cyclomatic complexity).
- **LLM review comments** — sends each changed file to a local [Ollama](https://ollama.com) model (`codellama` by default); a custom prompt can be supplied with `--ai-prompt` (use `{diff}` as the placeholder).
- **Rule-based checks and scoring** — flags `print` statements, TODOs and functions longer than 50 lines, and produces a 0–100 quality score weighted by issue type.
- **Batch review** — pass several PR numbers separated by commas.
- **Report export** — `review_report.md` and `review_report.pdf`.

## Tech Stack

Python · requests · Rich · pylint · bandit · radon · Ollama (local LLM) · fpdf2 · markdown2

## Architecture

```
interface/cli.py ──► git_integration/{github,gitlab,bitbucket}.py ──► PR diff
        │
        ├─► interface/diff_viewer.py        terminal diff view
        ├─► code_analysis/advanced.py       pylint · bandit · radon on added lines
        ├─► feedback/ai_feedback.py         Ollama /api/generate
        ├─► code_analysis/analyzer.py       rule-based findings
        └─► feedback/generator.py ──► feedback/exporter.py   report, score, .md/.pdf
```

## Getting Started

Requires Python 3.8+. For LLM feedback, install [Ollama](https://ollama.com/download) and pull a model:

```bash
ollama run codellama        # serves on http://localhost:11434
```

Then:

```bash
cd Codemate.ai/pr_review_agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# GitHub (token: a personal access token with repo read access)
python main.py --provider github --repo https://github.com/<owner>/<repo> --pr 12 --token <token>

# Several PRs at once
python main.py --provider github --repo https://github.com/<owner>/<repo> --pr 12,15,18 --token <token>

# GitLab
python main.py --provider gitlab --repo https://gitlab.com/<group>/<project> --pr 7 --token <token>

# Bitbucket (app password)
python main.py --provider bitbucket --repo https://bitbucket.org/<workspace>/<repo> --pr 3 --username <user> --token <app-password>
```

If Ollama is not running, the review still completes and the LLM section reports the connection error. The PR summary block is currently available for GitHub only.

## Testing

```bash
cd Codemate.ai/pr_review_agent
python -m unittest tests/test_core.py -v
```

The tests cover the rule-based diff analyzer, report generation and PR scoring.

## Extending

- New git providers: subclass `BaseGitProvider` in `git_integration/`.
- New rules: add checks in `code_analysis/analyzer.py`.
