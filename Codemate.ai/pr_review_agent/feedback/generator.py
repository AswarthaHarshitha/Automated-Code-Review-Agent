"""
Feedback generator for PR Review Agent
"""

class FeedbackGenerator:
    def __init__(self):
        pass

    def generate_report(self, analysis_result: dict) -> str:
        """
        Generate a human-readable feedback report from analysis result.
        :param analysis_result: Dict with feedback
        :return: String report
        """
        feedback = analysis_result.get('feedback', [])
        if not feedback:
            return "No issues found. Good job!"
        report = ["Pull Request Review Feedback:"]
        for item in feedback:
            report.append(f"Line {item['line']} [{item['type'].capitalize()}]: {item['message']}")
        return '\n'.join(report)

    def score_pr(self, analysis_result: dict) -> int:
        """
        Unique feature: Score the PR based on number and severity of issues.
        :param analysis_result: Dict with feedback
        :return: Integer score (higher is better)
        """
        base_score = 100
        feedback = analysis_result.get('feedback', [])
        penalty = 0
        for item in feedback:
            if item['type'] == 'design':
                penalty += 15
            elif item['type'] == 'style':
                penalty += 10
            else:
                penalty += 5
        return max(0, base_score - penalty)
