from feedback.ai_feedback import AIFeedback
"""
CLI interface for PR Review Agent
"""

import argparse

from git_integration.github import GitHubProvider
from git_integration.gitlab import GitLabProvider
from git_integration.bitbucket import BitbucketProvider
from code_analysis.analyzer import CodeDiffAnalyzer
from feedback.generator import FeedbackGenerator
from feedback.exporter import FeedbackExporter
from interface.diff_viewer import show_diff_with_highlighting
from code_analysis.advanced import AdvancedAnalyzer

def main_cli():
    parser = argparse.ArgumentParser(description="PR Review Agent CLI")
    parser.add_argument('--provider', choices=['github', 'gitlab', 'bitbucket'], required=True, help='Git server provider')
    parser.add_argument('--repo', required=True, help='Repository URL')
    parser.add_argument('--pr', required=True, help='Pull request ID/number or comma-separated list of PRs')
    parser.add_argument('--token', required=True, help='Access token for API (GitHub/GitLab) or Bitbucket app password')
    parser.add_argument('--username', required=False, help='Bitbucket username (required for Bitbucket)')
    parser.add_argument('--ai-prompt', required=False, help='Custom prompt for AI code review feedback')
    args = parser.parse_args()

    pr_list = [pr.strip() for pr in args.pr.split(',')]

    if args.provider == 'github':
        provider = GitHubProvider(args.token)
    elif args.provider == 'gitlab':
        provider = GitLabProvider(args.token)
    elif args.provider == 'bitbucket':
        if not args.username:
            print("Bitbucket requires --username and --token (app password)")
            return
        provider = BitbucketProvider(args.username, args.token)
    else:
        print("Unsupported provider.")
        return

    for pr_id in pr_list:
        print(f"\n================ PR #{pr_id} ================")
        if args.provider == 'github':
            pr_stats = provider.fetch_pr_stats(args.repo, pr_id)
            print("\n[PR Summary]")
            print(f"Files changed: {pr_stats['files_changed']}")
            print(f"Additions: {pr_stats['additions']}")
            print(f"Deletions: {pr_stats['deletions']}")
            print(f"Contributors: {', '.join(pr_stats['contributors']) if pr_stats['contributors'] else 'N/A'}")
        elif args.provider == 'gitlab':
            print("\n[PR Summary]")
            print("(PR summary for GitLab not yet implemented)")
        elif args.provider == 'bitbucket':
            print("\n[PR Summary]")
            print("(PR summary for Bitbucket not yet implemented)")

        diff = provider.fetch_pr_diff(args.repo, pr_id)
        print("\n[Diff with Syntax Highlighting]")
        show_diff_with_highlighting(diff, language="python")

        # Only analyze Python files in the diff for advanced analysis
        import re
        file_diffs = {}
        current_file = None
        for line in diff.splitlines():
            file_match = re.match(r'diff --git a/(.+) b/(.+)', line)
            if file_match:
                current_file = file_match.group(2)
                file_diffs[current_file] = []
            elif current_file and (line.startswith('+') and not line.startswith('+++')):
                file_diffs[current_file].append(line[1:])

        adv_analyzer = AdvancedAnalyzer()
        ai_prompt = args.ai_prompt or None
        ai_feedback = AIFeedback(prompt=ai_prompt)
        for fname, lines in file_diffs.items():
            if fname.endswith('.py') and lines:
                code = '\n'.join(lines)
                print(f"\n[Advanced Analysis for {fname}]")
                print("[Linting Report]")
                print(adv_analyzer.analyze_lint(code))
                print("[Security Report]")
                print(adv_analyzer.analyze_security(code))
                print("[Complexity Report]")
                print(adv_analyzer.analyze_complexity(code))
                print("[AI-Driven Feedback]")
                print(ai_feedback.review_code(code))
            elif lines:
                print(f"\n[Skipping advanced analysis for {fname} (not a Python file)]")
                print("[AI-Driven Feedback]")
                print(ai_feedback.review_code('\n'.join(lines)))

        analyzer = CodeDiffAnalyzer()
        analysis_result = analyzer.analyze_diff(diff)

        feedback_gen = FeedbackGenerator()
        report = feedback_gen.generate_report(analysis_result)
        score = feedback_gen.score_pr(analysis_result)

        print("\n" + report)
        print(f"\nPR Quality Score: {score}/100")

        # Export options
        exporter = FeedbackExporter()
        md_file = exporter.export_markdown(report)
        pdf_file = exporter.export_pdf(report)
        print(f"\nReview report exported as: {md_file}, {pdf_file}")
