"""
AI-driven feedback using Ollama local LLM API
"""
import requests

class AIFeedback:
    def __init__(self, model="codellama", prompt=None):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.custom_prompt = prompt

    def review_code(self, diff: str) -> str:
        prompt = self.custom_prompt or (
            "You are an expert code reviewer. Review the following code diff and provide constructive, actionable feedback for improvements, code quality, and possible bugs.\n"
            "If the diff is not code, say so.\n\n"
            f"Diff:\n{diff}\n"
        )
        if self.custom_prompt:
            prompt = prompt.replace("{diff}", diff)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.ollama_url, json=payload, timeout=120)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "[No AI feedback returned]").strip()
        except Exception as e:
            return f"[AI Feedback Error] {e}"
