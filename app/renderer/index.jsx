import React from 'react';
import ReactDOM from 'react-dom';
import Chat from './components/Chat';

function App() {

    const addTab = () => {
        const newTab = {
            id: nextTabId,
            url: 'https://duckduckgo.com',
            title: 'New Tab'
        };
        setTabs([...tabs, newTab]);
        setActiveTabId(nextTabId);
        setNextTabId(nextTabId + 1);
    };

    const closeTab = (tabId) => {
        if (tabs.length === 1) {
            addTab();
        }
        const newTabs = tabs.filter(tab => tab.id !== tabId);
        setTabs(newTabs);
        if (activeTabId === tabId) {
            setActiveTabId(newTabs[newTabs.length - 1].id);
        }
    };

    const handleTabClick = (tabId) => {
        setActiveTabId(tabId);
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
            <Chat />
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
