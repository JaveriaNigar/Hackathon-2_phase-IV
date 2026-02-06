'use client';

import React, { useEffect, useState } from 'react';
import { getCurrentUser } from '@/services/auth';
import { isAuthenticated } from '@/lib/auth';
import ChatWindow from '@/components/ChatInterface/ChatWindow';
import Sidebar from '@/components/ChatInterface/Sidebar';
import useChat from '@/hooks/useChat';
import apiClient, { chatApi } from '@/services/api';

interface Conversation {
    id: string;
    title?: string;
    created_at: string;
}

export default function AgentPage() {
    const [userId, setUserId] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const { messages, sendMessage, clearChat, setConversationId, conversationId, isLoading } = useChat(userId || '');

    const fetchConversations = async (uid: string) => {
        try {
            const response = await apiClient.get<Conversation[]>(`${uid}/conversations`);
            setConversations(response.data);
        } catch (error) {
            console.error('Error fetching conversations:', error);
        }
    };

    const handleDeleteConversation = async (id: string | number) => {
        if (!userId) return;
        if (!confirm('Are you sure you want to delete this chat?')) return;

        try {
            const convIdStr = String(id);
            await chatApi.deleteConversation(userId, convIdStr);
            setConversations(prev => prev.filter(c => c.id !== convIdStr));

            // If the current chat was deleted, clear the view
            if (conversationId === convIdStr) {
                clearChat();
            }
        } catch (error) {
            console.error('Failed to delete conversation:', error);
            alert('Failed to delete conversation. Please try again.');
        }
    };

    useEffect(() => {
        const checkAuth = async () => {
            if (!isAuthenticated()) {
                window.location.href = '/login';
                return;
            }

            try {
                const user = await getCurrentUser();
                setUserId(user.id);
                await fetchConversations(user.id);
            } catch (error) {
                console.error('Error fetching user:', error);
                window.location.href = '/login';
            } finally {
                setLoading(false);
            }
        };

        checkAuth();
    }, []);

    // Re-fetch conversations when a new one is created or message sent
    useEffect(() => {
        if (userId) {
            fetchConversations(userId);
        }
    }, [conversationId]);

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-background">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-ai-blue mx-auto"></div>
                    <p className="mt-4 text-foreground">Loading agent...</p>
                </div>
            </div>
        );
    }

    if (!userId) {
        return null;
    }

    return (
        <div className="h-screen w-screen flex overflow-hidden bg-background">
            {/* Sidebar */}
            <Sidebar
                conversations={conversations}
                onCreateNewChat={clearChat}
                onSelectConversation={(id: string | number) => setConversationId(String(id))}
                onDeleteConversation={handleDeleteConversation}
            />

            {/* Chat Window */}
            <div className="flex-1 flex flex-col relative bg-background">
                <ChatWindow
                    conversationId={userId}
                    messages={messages}
                    sendMessage={sendMessage}
                    clearChat={clearChat}
                    isLoading={isLoading}
                />
            </div>
        </div>
    );
}
