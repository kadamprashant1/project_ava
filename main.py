# main.py
import logging
from configparser import ConfigParser
from browser_manager import BrowserManager
from perception import PerceptionModule
from ollama_agent import OllamaAgent
from agent_orchestrator import WebAgent
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # --- Configuration ---
    config = ConfigParser()
    config.read('config.ini')

    # Create screenshots directory if it doesn't exist
    screenshot_dir = config.get('Agent', 'SCREENSHOT_DIR', fallback='./screenshots')
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # --- Initialization ---
    try:
        browser = BrowserManager(config['Browser'])
        perception = PerceptionModule(config)
        ollama = OllamaAgent(config['Ollama'])
        agent = WebAgent(config['Agent'], browser, perception, ollama)
    except Exception as e:
        logging.error(f"Failed to initialize modules: {e}")
        return

    # --- Goal Definition ---
    goal = "Find the current price of the latest iPhone on Apple's official website."
    start_url = "https://www.google.com" # Start from a search engine

    # --- Agent Execution ---
    try:
        result = agent.run(goal, start_url)
        logging.info(f"--- Final Result ---")
        logging.info(result)
    except Exception as e:
        logging.error(f"An unhandled exception occurred during agent execution: {e}")
    finally:
        # Ensure browser is closed even if agent.run() fails
        if 'browser' in locals() and browser.driver:
            browser.close_browser()

if __name__ == "__main__":
    main()
