import json

PROMPT_TEMPLATE = """
You are an AI agent controlling a web browser. You are given a user's goal and the current state of the web page. Your task is to create a JSON plan of actions to achieve the user's goal.

The available actions are:
- `goto(url)`: Navigates to a URL.
- `extract(selector)`: Extracts text from an element on the page.
- `summarize(text)`: Summarizes a piece of text.

User's goal: {goal}

Current page content:
{page_content}

Your JSON plan:
"""

def create_plan(prompt):
    """Creates a JSON action plan based on the user's prompt."""
    try:
        plan = json.loads(prompt)
        return plan
    except json.JSONDecodeError:
        return []
