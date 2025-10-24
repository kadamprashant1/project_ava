# perception.py
import logging
from bs4 import BeautifulSoup

class PerceptionModule:
    def __init__(self, config):
        self.config = config

    def get_page_summary(self, html, ollama_agent):
        soup = BeautifulSoup(html, 'html.parser')
        text_content = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'a', 'button', 'span']):
            text = tag.get_text(strip=True)
            if text:
                text_content.append(text)
        
        full_text = " ".join(text_content)
        # Truncate to avoid exceeding token limits
        max_length = 3000 
        if len(full_text) > max_length:
            full_text = full_text[:max_length] + "..."
            
        summary_prompt = f"Summarize the following webpage content in one sentence:
{full_text}"
        summary = ollama_agent.process_extracted_data("summary", summary_prompt)
        return summary

    def get_actionable_elements(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        actionable_elements = []
        id_counter = 1
        
        for tag in soup.find_all(['a', 'button', 'input', 'textarea', 'select']):
            if not tag.has_attr('disabled') and tag.get('type') != 'hidden':
                text = tag.get_text(strip=True) or tag.get('aria-label', '') or tag.get('name', '')
                
                element_type = tag.name
                if element_type == 'a':
                    id_prefix = 'L' # Link
                elif element_type == 'button':
                    id_prefix = 'B' # Button
                elif element_type in ['input', 'textarea', 'select']:
                    id_prefix = 'I' # Input
                else:
                    id_prefix = 'E' # Element
                    
                element_id = f"{id_prefix}{id_counter}"
                
                actionable_elements.append({
                    "id": element_id,
                    "type": element_type,
                    "text": text[:100], # Truncate long text
                    "selector": f"#{tag['id']}" if tag.has_attr('id') else f"{tag.name}[{id_counter-1}]" # simplified selector
                })
                id_counter += 1
        return actionable_elements

    def get_full_page_state(self, browser, ollama_agent):
        html = browser.get_page_source()
        url = browser.get_current_url()
        
        summary = self.get_page_summary(html, ollama_agent)
        actionable_elements = self.get_actionable_elements(html)
        
        page_state = {
            "url": url,
            "summary": summary,
            "actionable_elements": actionable_elements
        }
        
        # Optional: Add visual description if multimodal is enabled
        # screenshot_path = "./screenshots/current_view.png"
        # browser.take_screenshot(screenshot_path)
        # visual_description = self.get_visual_description(screenshot_path, ollama_agent)
        # page_state["visual_description"] = visual_description
        
        return page_state

    # Optional multimodal method
    # def get_visual_description(self, screenshot_path, ollama_agent):
    #     # Requires a multimodal model like llava
    #     # Convert image to base64 and send to ollama
    #     pass
