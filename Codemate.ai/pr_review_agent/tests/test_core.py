import unittest
from code_analysis.analyzer import CodeDiffAnalyzer
from feedback.generator import FeedbackGenerator

class TestCodeDiffAnalyzer(unittest.TestCase):
    def test_analyze_diff_print(self):
        diff = '+print("Hello")\n+def foo():\n    pass\n'
        analyzer = CodeDiffAnalyzer()
        result = analyzer.analyze_diff(diff)
        feedback = result['feedback']
        self.assertTrue(any('print' in f['message'] for f in feedback))

    def test_analyze_diff_todo(self):
        diff = '+# TODO: fix this\n+def bar():\n    pass\n'
        analyzer = CodeDiffAnalyzer()
        result = analyzer.analyze_diff(diff)
        feedback = result['feedback']
        self.assertTrue(any('TODO' in f['message'] for f in feedback))

class TestFeedbackGenerator(unittest.TestCase):
    def test_score_pr(self):
        gen = FeedbackGenerator()
        analysis_result = {'feedback': [
            {'line': 1, 'type': 'design', 'message': 'Large function'},
            {'line': 2, 'type': 'style', 'message': 'Print statement'},
            {'line': 3, 'type': 'other', 'message': 'Other'}
        ]}
        score = gen.score_pr(analysis_result)
        self.assertEqual(score, 100 - 15 - 10 - 5)

    def test_generate_report_no_issues(self):
        gen = FeedbackGenerator()
        analysis_result = {'feedback': []}
        report = gen.generate_report(analysis_result)
        self.assertIn('No issues found', report)

if __name__ == '__main__':
    unittest.main()
