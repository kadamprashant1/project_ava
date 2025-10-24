# ollama_agent.py
import ollama
import json
import logging

class OllamaAgent:
    def __init__(self, config):
        self.client = ollama.Client(host=config.get('HOST'))
        self.model = config.get('MODEL')
        self.temperature = config.getfloat('TEMPERATURE')
        self.max_tokens = config.getint('MAX_TOKENS')

    def _generate(self, prompt, is_json=False):
        try:
            messages = [{'role': 'user', 'content': prompt}]
            
            response = self.client.chat(
                model=self.model,
                messages=messages,
                stream=False,
                options={
                    'temperature': self.temperature,
                    'num_predict': self.max_tokens
                }
            )
            content = response['message']['content']
            
            if is_json:
                # Basic cleaning of the response to extract JSON
                content = content[content.find('{'):content.rfind('}')+1]
                return json.loads(content)
            return content
        except Exception as e:
            logging.error(f"Error communicating with Ollama: {e}")
            if is_json:
                return {"thought": "Error generating action.", "action_type": "ERROR", "action_args": {"error": str(e)}}
            return f"Error: {e}"

    def generate_action(self, goal, page_state, history):
        system_prompt = '''
You are an autonomous web browsing agent that can perceive, reason, and act.
Your goal is to achieve the user's objective by navigating and interacting with websites.

Based on the current page state and your history, decide the next best action to take.

Available Actions:
1. NAVIGATE_TO(url): Go to a specific URL.
2. CLICK(element_id): Click on an interactive element (link, button, etc.) identified by its ID.
3. TYPE(element_id, text): Type text into an input field.
4. EXTRACT_DATA(query): Use this when the information needed to answer the goal is present on the current page. The query should be a question for an LLM to answer based on the page content.
5. FINISH(result_data): Use this action when you have successfully found the answer to the user's goal.
6. SCROLL(direction): Scroll the page 'up' or 'down'.

Always respond with a JSON object in the following format:
{"thought": "Your reasoning for the chosen action.", "action_type": "ACTION_NAME", "action_args": {"arg1": "value1", ...}}
'''
        
        prompt = f'''
{system_prompt}

**User Goal:**
{goal}

**Current Page State:**
{json.dumps(page_state, indent=2)}

**Your History (Recent Actions):**
{json.dumps(history, indent=2)}

**Your Task:**
Based on all the information above, what is your next action?
Respond with ONLY the JSON for your next action.
'''
        return self._generate(prompt, is_json=True)

    def process_extracted_data(self, query, text):
        prompt = f"Based on the following text, please answer this query: '{query}'\n\nText:\n{text}"
        return self._generate(prompt)
