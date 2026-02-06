import React, { useState, useEffect, useRef } from 'react';
import { Message } from '../../hooks/useChat';

interface ChatWindowProps {
  conversationId: string;
  messages: Message[];
  sendMessage: (message: string) => Promise<string | undefined | void>;
  clearChat: () => void;
  isLoading: boolean;
}

const ChatWindow = ({ conversationId, messages, sendMessage, clearChat, isLoading }: ChatWindowProps) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    await sendMessage(inputValue);
    setInputValue('');
  };

  return (
    <div className="flex flex-col h-full bg-background">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto p-4 bg-background">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`mb-4 p-4 rounded-xl w-fit max-w-[75%] ${message.role === 'user'
              ? 'bg-gradient-to-r from-ai-blue to-ai-purple text-white ml-auto'
              : 'bg-card-bg text-foreground mr-auto'
              }`}
          >
            <div className="whitespace-pre-wrap">{message.content}</div>
          </div>
        ))}
        {isLoading && (
          <div className="mb-4 p-3 rounded-lg bg-card-bg text-foreground mr-auto">
            <div>Thinking...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="p-4 pb-8 bg-background">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message here..."
            className="flex-1 input-animated focus:outline-none"
            disabled={isLoading}
          />
          <button
            type="submit"
            className="btn-ai-gradient rounded-lg ripple-effect hover:opacity-90 disabled:opacity-50"
            disabled={isLoading || !inputValue.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatWindow;