import React from 'react';
import { Message } from '../../hooks/useChat';

interface MessageListProps {
    messages: Message[];
    isLoading: boolean;
}

const MessageList = ({ messages, isLoading }: MessageListProps) => {
    return (
        <div className="overflow-y-auto flex-1 p-4">
            {messages.length > 0 && (
                <div className="space-y-4">
                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`p-3 rounded-lg max-w-3/4 ${message.role === 'user'
                                ? 'bg-blue-500 text-white ml-auto'
                                : 'bg-gray-200 text-gray-800 mr-auto'
                                }`}
                        >
                            <div className="whitespace-pre-wrap">{message.content}</div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="p-3 rounded-lg bg-gray-200 text-gray-800 mr-auto">
                            <div>Thinking...</div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default MessageList;
