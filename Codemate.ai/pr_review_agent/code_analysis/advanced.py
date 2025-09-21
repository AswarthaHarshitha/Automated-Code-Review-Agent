"""
Advanced code analysis: linting, security, and complexity
"""
import tempfile
import subprocess
import os
import sys

class AdvancedAnalyzer:
    def __init__(self):
        pass

    def _get_executable(self, name):
        # Use the Scripts directory in the current venv if available
        venv_path = os.environ.get('VIRTUAL_ENV')
        if venv_path:
            exe = os.path.join(venv_path, 'Scripts', f'{name}.exe')
            if os.path.exists(exe):
                return exe
        # Fallback to just the name
        return name

    def analyze_lint(self, code: str) -> str:
        """Run pylint on the code and return the report."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w', encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name
        try:
            pylint_path = self._get_executable('pylint')
            result = subprocess.run([pylint_path, temp_path, '--disable=all', '--enable=E,W,C,R'], capture_output=True, text=True)
            return result.stdout
        finally:
            os.remove(temp_path)

    def analyze_security(self, code: str) -> str:
        """Run bandit for security checks and return the report."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w', encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name
        try:
            bandit_path = self._get_executable('bandit')
            result = subprocess.run([bandit_path, '-r', temp_path, '-q'], capture_output=True, text=True)
            return result.stdout
        finally:
            os.remove(temp_path)

    def analyze_complexity(self, code: str) -> str:
        """Run radon to check cyclomatic complexity and return the report."""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w', encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name
        try:
            radon_path = self._get_executable('radon')
            result = subprocess.run([radon_path, 'cc', temp_path, '-s'], capture_output=True, text=True)
            return result.stdout
        finally:
            os.remove(temp_path)
