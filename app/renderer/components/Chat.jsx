import React, { useState } from 'react';
import MessageList from './MessageList';

function Chat() {
    const [message, setMessage] = useState('');
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = React.useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    React.useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!message.trim() || isLoading) return;

        const newMessage = { role: 'user', content: message };
        setMessages(prev => [...prev, newMessage]);
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: message }),
            });

            const data = await response.json();
            
            if (response.ok) {
                (prev => [...prev, { 
                    role: 'assistant', 
                    content: data.response,
                    ...(data.execution_result && {
                        execution: data.execution_result
                    })
                }]);
            } else {
                console.error('Error:', data);
                setMessages(prev => [...prev, { role: 'error', content: 'Failed to get response' }]);
            }
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [...prev, { role: 'error', content: 'Network error' }]);
        } finally {
            setIsLoading(false);
            setMessage('');
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <h3>Chat with Gemma</h3>
            </div>
            <MessageList 
                messages={messages}
                isLoading={isLoading}
                messagesEndRef={messagesEndRef}
            />
            <form onSubmit={handleSubmit} className="chat-input">
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Type your message..."
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Sending...' : 'Send'}
                </button>
            </form>
        </div>
    );
}

export default Chat;