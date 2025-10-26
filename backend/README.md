# Backend

This directory contains the Python backend for the agentic browser. It is a FastAPI server that uses Playwright to control a web browser and Ollama to provide AI-powered agentic capabilities.

## Endpoints

The following endpoints are available:

*   `POST /open`: Opens a URL in the browser.
*   `GET /snapshot`: Takes a snapshot of the current page, including the text and links.
*   `POST /get_page_content`: Gets the full HTML content of the current page.
*   `POST /agent/plan`: Creates a plan for the AI agent to execute based on a user prompt.
*   `POST /agent/execute`: Executes a plan created by the AI agent.

## Usage

To run the backend server, navigate to this directory and run the following command:

```
uvicorn agent_server:app --reload
```

The server will be available at `http://127.0.0.1:8000`.
