import { useState, useEffect } from 'react';
import { getToken } from '@/lib/auth';
import apiClient from '@/services/api';

export interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
}

interface ToolCall {
  name: string;
  arguments: any;
}

interface ChatResponse {
  conversation_id: string;
  response: string;
  tool_calls?: ToolCall[];
}

const useChat = (userId: string, initialConversationId?: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | undefined>(initialConversationId);

  // Load messages for the conversation if conversationId is provided
  useEffect(() => {
    const loadMessages = async () => {
      if (!conversationId || conversationId === 'new') {
        setMessages([]);
        return;
      }

      setIsLoading(true);
      try {
        const response = await apiClient.get<Message[]>(`${userId}/conversations/${conversationId}/messages`);
        setMessages(response.data);
      } catch (error) {
        console.error('Error loading messages:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadMessages();
  }, [userId, conversationId]);

  const executeToolCall = async (userId: string, toolCall: ToolCall) => {
    try {
      console.log('Backend requested tool execution (frontend side):', toolCall.name, toolCall.arguments);

      switch (toolCall.name) {
        case 'add_task':
          // Handled by backend. Do not duplicate.
          console.log('Task addition handled by backend.');
          break;
        case 'list_tasks':
          // Handled by backend response text (if agent obeys), or by page refresh.
          // Future improvement: Trigger a global refresh event here.
          break;
        case 'complete_task':
          // Handled by backend.
          break;
        case 'delete_task':
          // Handled by backend.
          break;
        case 'update_task':
          // Handled by backend.
          break;
        default:
          console.warn(`Unknown tool call: ${toolCall.name}`);
      }

      // Trigger a global event to notify other components that tasks may have changed
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('tasksChanged'));
      }
    } catch (error) {
      console.error(`Error executing tool call ${toolCall.name}:`, error);
    }
  };


  const sendMessage = async (messageText: string) => {
    setIsLoading(true);

    try {
      if (!userId) {
        console.error('Cannot send message: User ID is missing');
        return;
      }

      // Add user message to the UI immediately for responsiveness
      const tempUserMsg: Message = {
        id: Date.now(),
        role: 'user',
        content: messageText,
      };
      setMessages(prev => [...prev, tempUserMsg]);

      // Call the backend API
      const response = await apiClient.post<ChatResponse>(`${userId}/chat`, {
        message: messageText,
        conversation_id: conversationId === 'new' ? undefined : conversationId
      });

      const newConvId = response.data.conversation_id;
      if (conversationId !== newConvId) {
        setConversationId(newConvId);
      }

      // Refresh messages from backend to get official IDs and correct state
      const messagesResponse = await apiClient.get<Message[]>(`${userId}/conversations/${newConvId}/messages`);
      setMessages(messagesResponse.data);

      // Execute any tool calls if present
      if (response.data.tool_calls && response.data.tool_calls.length > 0) {
        for (const toolCall of response.data.tool_calls) {
          await executeToolCall(userId, toolCall);
        }
      }

      return newConvId;
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId('new');
  };

  return {
    messages,
    sendMessage,
    clearChat,
    setConversationId,
    conversationId,
    isLoading,
  };
};

export default useChat;