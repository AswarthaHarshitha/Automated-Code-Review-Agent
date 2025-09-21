"""
Inline diff viewer with syntax highlighting using Rich
"""
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text

console = Console()

def show_diff_with_highlighting(diff_text: str, language: str = "python"):
    """
    Display a unified diff with syntax highlighting for added/removed lines.
    :param diff_text: Unified diff as a string
    :param language: Programming language for syntax highlighting
    """
    lines = diff_text.splitlines()
    for line in lines:
        if line.startswith('+') and not line.startswith('+++'):
            syntax = Syntax(line[1:], language, theme="monokai", line_numbers=False)
            console.print(Panel(syntax, style="green"))
        elif line.startswith('-') and not line.startswith('---'):
            syntax = Syntax(line[1:], language, theme="monokai", line_numbers=False)
            console.print(Panel(syntax, style="red"))
        else:
            console.print(Text(line, style="white"))
