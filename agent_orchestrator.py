# agent_orchestrator.py
import logging
import time
from collections import deque

class WebAgent:
    def __init__(self, config, browser_manager, perception_module, ollama_agent):
        self.config = config
        self.browser = browser_manager
        self.perception = perception_module
        self.ollama = ollama_agent
        self.max_iterations = self.config.getint('MAX_ITERATIONS')
        self.history = deque(maxlen=10) # Keep a history of recent actions

    def run(self, goal, start_url):
        logging.info(f"Starting agent with goal: {goal}")
        self.browser.go_to_url(start_url)
        
        for i in range(self.max_iterations):
            logging.info(f"--- Iteration {i+1}/{self.max_iterations} ---")
            
            try:
                page_state = self.perception.get_full_page_state(self.browser, self.ollama)
                
                decision = self.ollama.generate_action(goal, page_state, list(self.history))
                logging.info(f"LLM Decision: {decision}")
                
                self.history.append(decision)
                
                action_type = decision.get('action_type')
                action_args = decision.get('action_args', {})

                if action_type == "NAVIGATE_TO":
                    self.browser.go_to_url(action_args['url'])
                elif action_type == "CLICK":
                    # This is a simplification. We need to map element_id to a real selector.
                    # For now, we assume a simple mapping which is not robust.
                    # A better implementation would use the selector from get_actionable_elements
                    logging.warning("CLICK action is simplified and may not work reliably.")
                    # Example: self.browser.click_element(By.ID, action_args['element_id'])
                    pass 
                elif action_type == "TYPE":
                    logging.warning("TYPE action is simplified and may not work reliably.")
                    # Example: self.browser.type_text(By.ID, action_args['element_id'], action_args['text'])
                    pass
                elif action_type == "SCROLL":
                    if action_args.get('direction') == 'down':
                        self.browser.scroll_to_bottom()
                    else: # 'up'
                        self.browser.execute_script("window.scrollTo(0, 0);")
                elif action_type == "EXTRACT_DATA":
                    source = self.browser.get_page_source()
                    extracted_info = self.ollama.process_extracted_data(action_args['query'], source)
                    self.history.append({"action_type": "OBSERVATION", "data": extracted_info})
                    logging.info(f"Extracted data: {extracted_info}")
                elif action_type == "FINISH":
                    logging.info("Agent has finished the task.")
                    self.browser.close_browser()
                    return action_args.get("result_data", "No result data provided.")
                elif action_type == "ERROR":
                    logging.error(f"LLM returned an error: {action_args.get('error')}")
                    time.sleep(5) # Wait before retrying
                else:
                    logging.warning(f"Unknown action type: {action_type}")

                time.sleep(self.config.getint('ACTION_TIMEOUT', 3)) # Human-like delay

            except Exception as e:
                logging.error(f"An error occurred in the agent loop: {e}")
                self.browser.take_screenshot("error_screenshot.png")
                time.sleep(5)

        logging.warning("Agent reached max iterations without finishing.")
        self.browser.close_browser()
        return "Max iterations reached."
