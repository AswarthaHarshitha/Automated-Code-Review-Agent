"""
Code Diff Analyzer for PR Review Agent
"""

import difflib

class CodeDiffAnalyzer:
    def __init__(self):
        pass

    def analyze_diff(self, diff_text: str) -> dict:
        """
        Analyze the diff and return structured feedback.
        :param diff_text: Unified diff as a string
        :return: Dict with feedback
        """
        feedback = []
        lines = diff_text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith('+') and not line.startswith('+++'):
                if 'print(' in line:
                    feedback.append({
                        'line': i+1,
                        'type': 'style',
                        'message': 'Avoid using print statements in production code.'
                    })
                if 'TODO' in line:
                    feedback.append({
                        'line': i+1,
                        'type': 'comment',
                        'message': 'Address TODO comments before merging.'
                    })
        # Unique feature: Detect large functions added in PR
        large_func_lines = self._detect_large_functions(lines)
        for func in large_func_lines:
            feedback.append({
                'line': func['line'],
                'type': 'design',
                'message': f"Function '{func['name']}' is quite large ({func['length']} lines). Consider refactoring."
            })
        return {'feedback': feedback}

    def _detect_large_functions(self, lines, threshold=50):
        """
        Detects large functions in the diff (unique feature).
        """
        func_lines = []
        in_func = False
        func_name = ''
        func_start = 0
        count = 0
        for i, line in enumerate(lines):
            if line.startswith('+def '):
                in_func = True
                func_name = line.split('def ')[1].split('(')[0]
                func_start = i+1
                count = 1
            elif in_func and (line.startswith('+') or line.startswith(' ')):
                count += 1
                if count > threshold:
                    func_lines.append({'name': func_name, 'line': func_start, 'length': count})
                    in_func = False
            elif in_func and not (line.startswith('+') or line.startswith(' ')):
                in_func = False
        return func_lines
