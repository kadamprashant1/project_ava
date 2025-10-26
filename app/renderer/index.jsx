import React, { useState } from 'react';
import ReactDOM from 'react-dom';

function App() {
    const [url, setUrl] = useState('https://www.google.com');
    const [prompt, setPrompt] = useState('');
    const [messages, setMessages] = useState([]);

    const handleUrlChange = (event) => {
        if (event.key === 'Enter') {
            setUrl(event.target.value);
        }
    };

    const handlePromptChange = (event) => {
        setPrompt(event.target.value);
    };

    const handleSendPrompt = async () => {
        const response = await fetch('http://127.0.0.1:8000/agent/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        });
        const data = await response.json();
        setMessages([...messages, { type: 'user', text: prompt }, { type: 'agent', text: JSON.stringify(data.plan) }]);

        const executeResponse = await fetch('http://127.0.0.1:8000/agent/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ plan: data.plan }),
        });
        const executeData = await executeResponse.json();
        setMessages([...messages, { type: 'user', text: prompt }, { type: 'agent', text: JSON.stringify(data.plan) }, { type: 'agent', text: JSON.stringify(executeData) }]);
    };

    return (
        <div className="app-container">
            <div className="main-content">
                <div className="address-bar">
                    <input type="text" placeholder="Enter URL or search..." onKeyDown={handleUrlChange} />
                </div>
                <div className="webview-container">
                    <webview id="webview" src={url}></webview>
                </div>
            </div>
            <div className="chat-panel">
                <div className="chat-messages">
                    {messages.map((message, index) => (
                        <div key={index} className={`message ${message.type}`}>
                            {message.text}
                        </div>
                    ))}
                </div>
                <div className="chat-input">
                    <input type="text" placeholder="Ask the agent..." value={prompt} onChange={handlePromptChange} />
                    <button onClick={handleSendPrompt}>Send</button>
                </div>
            </div>
        </div>
    );
}

ReactDOM.render(<App />, document.getElementById('root'));
