from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from ollama_client import get_ollama_response
from planner import create_plan, execute_plan

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLBody(BaseModel):
    url: str

class PlanBody(BaseModel):
    prompt: str

class ExecuteBody(BaseModel):
    plan: list

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        # Get initial response from Ollama
        llm_response = get_ollama_response(request.prompt)
        
        # Create a plan from the response
        plan = create_plan(llm_response)
        
        # Execute the plan if any actions were generated
        if plan:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                result = execute_plan(plan, page)
                browser.close()
                return {
                    "response": llm_response,
                    "plan": plan,
                    "execution_result": result
                }
        else:
            # If no plan was created, just return the Ollama response
            return {"response": llm_response}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/open")
def open_url(body: URLBody):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(body.url)
        browser.close()
    return {"status": f"URL {body.url} opened successfully"}

@app.get("/snapshot")
def snapshot(body: URLBody):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(body.url)
        html = page.content()
        browser.close()
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = "\n".join(chunk for chunk in chunks if chunk)
        links = [link.get('href') for link in soup.find_all('a')]
        return {"text": text, "links": links}

@app.post("/get_page_content")
def get_page_content(body: URLBody):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(body.url)
        content = page.content()
        browser.close()
        return {"content": content}

@app.post("/agent/plan")
def agent_plan(body: PlanBody):
    response = get_ollama_response(body.prompt)
    plan = create_plan(response)
    return {"plan": plan}

@app.post("/agent/execute")
def agent_execute(body: ExecuteBody):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for action in body.plan:
            if action['action'] == 'goto':
                page.goto(action['url'])
            elif action['action'] == 'extract':
                html = page.content()
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = "\n".join(chunk for chunk in chunks if chunk)
                return {"text": text}
        browser.close()
    return {"execution": "plan executed"}
