from fastapi import FastAPI
from pydantic import BaseModel
from playwright.async_api import async_playwright
import asyncio
from ollama_client import get_ollama_response
from planner import create_plan

app = FastAPI()

class URLBody(BaseModel):
    url: str

class PlanBody(BaseModel):
    prompt: str

class ExecuteBody(BaseModel):
    plan: list

@app.post("/open")
async def open_url(body: URLBody):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(body.url)
        await browser.close()
    return {"status": f"URL {body.url} opened successfully"}

@app.get("/snapshot")
async def snapshot(body: URLBody):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(body.url)
        html = await page.content()
        await browser.close()
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
async def get_page_content(body: URLBody):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(body.url)
        content = await page.content()
        await browser.close()
        return {"content": content}

@app.post("/agent/plan")
async def agent_plan(body: PlanBody):
    response = get_ollama_response(body.prompt)
    plan = create_plan(response)
    return {"plan": plan}

@app.post("/agent/execute")
async def agent_execute(body: ExecuteBody):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for action in body.plan:
            if action['action'] == 'goto':
                await page.goto(action['url'])
            elif action['action'] == 'extract':
                html = await page.content()
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = "\n".join(chunk for chunk in chunks if chunk)
                return {"text": text}
        await browser.close()
    return {"execution": "plan executed"}
