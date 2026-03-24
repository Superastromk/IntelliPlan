import os
import requests
import re
from PyQt5.QtCore import QThread, pyqtSignal

# Load API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Base URL for OpenRouter
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Model to use (Free version on OpenRouter)
# 'google/gemini-2.0-flash-lite-001' is typically faster if available for free, 
# otherwise 'openrouter/free' will route to best available.
MODEL = "google/gemini-2.0-flash-lite-001"


class AIWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, prompt):
        super().__init__()
        self.prompt = prompt

    def run(self):
        try:
            response = ask_ai(self.prompt)
            if response.startswith("AI Error:"):
                self.error.emit(response)
            else:
                self.finished.emit(response)
        except Exception as e:
            self.error.emit(f"AI Error: {str(e)}")


def clean_ai_response(response: str):
    """
    Cleans the AI response by ensuring it's properly formatted for Markdown
    and handles common LaTeX/formatting symbol issues.
    """
    if not response:
        return ""

    # 1. Handle common LaTeX artifacts
    # Replace \( ... \) with $ ... $ and \[ ... \] with $$ ... $$ for standard Markdown feel
    response = re.sub(r'\\\((.*?)\\\)', r'$\1$', response)
    response = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', response, flags=re.DOTALL)

    # 2. Basic cleanup for any weird symbols/artifacts
    response = response.strip()

    # 3. Handle potential LaTeX formatting for better readability
    # Ensure headers have a newline before them
    response = re.sub(r'(?<!\n)#', r'\n#', response)
    response = re.sub(r'(\n{3,})', r'\n\n', response) # Max 2 newlines

    return response


def ask_ai(prompt: str):
    try:
        response = requests.post(
            BASE_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost",
                "X-Title": "StudyMK"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30 # Add timeout to prevent indefinite hangs
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"AI Error: {str(e)}"

    # If OpenRouter returned an error
    if "error" in data:
        return f"AI Error: {data['error'].get('message', 'Unknown error')}"

    # If choices exist (normal case)
    if "choices" in data:
        content = data["choices"][0]["message"]["content"]
        return clean_ai_response(content)

    # Fallback
    return "AI returned an unexpected response."