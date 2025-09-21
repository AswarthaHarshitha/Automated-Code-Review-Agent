"""
Export review feedback as Markdown or PDF
"""
from fpdf import FPDF
import markdown2

class FeedbackExporter:
    def __init__(self):
        pass

    def export_markdown(self, report: str, filename: str = "review_report.md"):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        return filename

    def export_pdf(self, report: str, filename: str = "review_report.pdf"):
        # Convert markdown to HTML, then to plain text for PDF
        html = markdown2.markdown(report)
        text = self._html_to_text(html)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in text.split('\n'):
            pdf.cell(0, 10, line, ln=1)
        pdf.output(filename)
        return filename

    def _html_to_text(self, html: str) -> str:
        # Simple HTML to text conversion for PDF export
        import re
        text = re.sub('<[^<]+?>', '', html)
        return text
