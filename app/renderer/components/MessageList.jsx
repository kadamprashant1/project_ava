import React from 'react';
import './MessageList.css';

function ChatMessage({ message }) {
    const { role, content } = message;
    const isUser = role === 'user';
    const label = isUser ? 'You' : 'Gemma';

    return (
        <div className={`message-wrapper ${role}`}>
            <div className="message-label">{label}</div>
            <div className={`message ${role}`}>
                {content}
            </div>
        </div>
    );
}

function MessageList({ messages, isLoading, messagesEndRef }) {
    return (
        <div className="messages-container">
            {messages.map((msg, index) => (
                <ChatMessage key={index} message={msg} />
            ))}
            {isLoading && (
                <div className="message-wrapper assistant">
                    <div className="message-label">Gemma</div>
                    <div className="message loading">
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                </div>
            )}
            <div ref={messagesEndRef} />
        </div>
    );
}

export default MessageList;