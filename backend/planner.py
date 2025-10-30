from typing import List, Dict, Any
import json
import time

PROMPT_TEMPLATE = """
You are an AI agent controlling a web browser. Generate a plan to accomplish the user's request.

Available actions:
1. goto(url): Navigate to a URL
2. click(selector): Click an element
3. type(selector, text): Type text into an input field
4. extract(selector): Extract text from elements
5. scroll(direction): Scroll the page (up/down)
6. back(): Go back one page
7. forward(): Go forward one page
8. refresh(): Refresh the current page
9. wait(seconds): Wait for a specified time
10. search(query): Search using DuckDuckGo

Format your response as a JSON array of actions. Each action should have:
- "action": The name of the action to perform
- "params": Parameters for the action

Example:
[
    {"action": "goto", "params": {"url": "https://example.com"}},
    {"action": "type", "params": {"selector": "#search", "text": "query"}},
    {"action": "click", "params": {"selector": "#submit"}}
]

User request: {prompt}
"""

def create_plan(prompt: str) -> List[Dict[str, Any]]:
    """Creates a structured action plan based on the user's prompt."""
    try:
        # If the prompt is already in JSON format, parse it directly
        if prompt.strip().startswith('[') and prompt.strip().endswith(']'):
            return json.loads(prompt)
        
        # For natural language prompts, create a basic plan
        if 'search' in prompt.lower() or 'look up' in prompt.lower():
            search_query = prompt.replace('search', '').replace('look up', '').strip()
            return [
                {
                    "action": "search",
                    "params": {"query": search_query}
                }
            ]
        elif 'go to' in prompt.lower() or 'visit' in prompt.lower():
            url = prompt.replace('go to', '').replace('visit', '').strip()
            if not url.startswith('http'):
                url = 'https://' + url
            return [
                {
                    "action": "goto",
                    "params": {"url": url}
                }
            ]
        else:
            # Default to a DuckDuckGo search for the prompt
            return [
                {
                    "action": "search",
                    "params": {"query": prompt}
                }
            ]
    except json.JSONDecodeError:
        return []

def execute_plan(plan: List[Dict[str, Any]], browser) -> Dict[str, Any]:
    """Executes a plan and returns the results."""
    results = []
    try:
        for step in plan:
            action = step.get('action')
            params = step.get('params', {})
            
            if action == 'goto':
                browser.goto(params['url'])
                results.append(f"Navigated to {params['url']}")
            elif action == 'search':
                search_url = f"https://duckduckgo.com/?q={params['query']}"
                browser.goto(search_url)
                results.append(f"Searched for {params['query']}")
            elif action == 'click':
                browser.click(params['selector'])
                results.append(f"Clicked element {params['selector']}")
            elif action == 'type':
                browser.type(params['selector'], params['text'])
                results.append(f"Typed {params['text']}")
            elif action == 'extract':
                element = browser.query_selector(params['selector'])
                if element:
                    text = element.text_content()
                    results.append(f"Extracted: {text}")
                else:
                    results.append(f"Could not find element: {params['selector']}")
            elif action == 'scroll':
                if params['direction'] == 'down':
                    browser.evaluate("window.scrollBy(0, 500)")
                else:
                    browser.evaluate("window.scrollBy(0, -500)")
                results.append(f"Scrolled {params['direction']}")
            elif action == 'wait':
                import time
                time.sleep(float(params['seconds']))
                results.append(f"Waited {params['seconds']} seconds")
            
    except Exception as e:
        results.append(f"Error: {str(e)}")
    
    return {"results": results}
