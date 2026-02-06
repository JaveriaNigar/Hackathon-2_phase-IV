import React, { useState, useEffect, useRef } from 'react';

interface Conversation {
    id: string | number;
    title?: string;
    created_at: string;
}

interface SidebarProps {
    conversations: Conversation[];
    onCreateNewChat: () => void;
    onSelectConversation: (id: string | number) => void;
    onDeleteConversation: (id: string | number) => void;
}

const Sidebar = ({ conversations, onCreateNewChat, onSelectConversation, onDeleteConversation }: SidebarProps) => {
    const [menuOpenId, setMenuOpenId] = useState<string | number | null>(null);
    const menuRef = useRef<HTMLDivElement>(null);

    // Close menu when clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setMenuOpenId(null);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const toggleMenu = (e: React.MouseEvent, id: string | number) => {
        e.stopPropagation();
        setMenuOpenId(menuOpenId === id ? null : id);
    };

    const handleDelete = (e: React.MouseEvent, id: string | number) => {
        e.stopPropagation();
        onDeleteConversation(id);
        setMenuOpenId(null);
    };

    return (
        <div className="w-64 bg-card-bg p-4 flex flex-col h-full">
            {/* Top Buttons Section */}
            <div className="space-y-3 mb-6">
                {/* ... Dashboard Button ... */}
                <button
                    onClick={() => window.location.href = '/dashboard'}
                    className="w-full btn-ai-gradient flex items-center justify-center gap-2 mb-3"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M14.5 3a.5.5 0 0 1 .5.5v9a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h13zm-13-1A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-9A1.5 1.5 0 0 0 14.5 2h-13z" />
                        <path d="M3 5.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5zM3 8a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9A.5.5 0 0 1 3 8zm0 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z" />
                    </svg>
                    Dashboard
                </button>

                <button
                    onClick={onCreateNewChat}
                    className="w-full btn-ai-gradient flex items-center justify-center gap-2"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z" />
                    </svg>
                    New Chat
                </button>

                <button
                    className="w-full bg-transparent hover:border-ai-blue text-foreground p-3 rounded-xl flex items-center gap-2 transition-all duration-300 hover:shadow-[0_0_15px_rgba(14,165,233,0.15)] group"
                    onClick={() => { /* Placeholder for search functionality */ }}
                >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="text-gray-400 group-hover:text-ai-blue transition-colors" viewBox="0 0 16 16">
                        <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                    </svg>
                    <span className="text-gray-400 group-hover:text-foreground transition-colors">Search Chat</span>
                </button>
            </div>

            {/* Your Chats Header */}
            <div className="mb-2">
                <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider pl-2">Your Chats</h3>
            </div>


            {/* Conversations List */}
            <div className="flex-1 overflow-y-auto pr-1 custom-scrollbar">
                {conversations.length > 0 ? (
                    <ul className="space-y-2">
                        {conversations.map((conversation) => (
                            <li key={conversation.id} className="relative">
                                <div className="group w-full p-2 rounded-xl hover:bg-white/5 transition-colors duration-200 flex items-center gap-2 cursor-pointer"
                                    onClick={() => onSelectConversation(conversation.id)}>

                                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-ai-cyan/20 to-ai-blue/20 flex items-center justify-center text-ai-blue group-hover:scale-110 transition-transform duration-300 flex-shrink-0">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                                            <path d="M2.678 11.894a1 1 0 0 1 .287.801 10.97 10.97 0 0 1-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 0 1 .71-.074A8.06 8.06 0 0 0 8 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894zm-.493 3.905a21.682 21.682 0 0 1-.713.129c-.2.032-.352-.176-.273-.362a9.68 9.68 0 0 0 .244-.697 1.002 1.002 0 0 0-.804-1.127A5.4 5.4 0 0 1 1 11.05a5.388 5.388 0 0 1 0-1.075 5.516 5.516 0 0 1 1.706-5.004c.882-.882 2.067-1.37 3.32-1.37 2.39 0 4.544 1.793 4.965 4.145.42 2.352-1.028 4.672-3.376 5.253a5.539 5.539 0 0 1-1.082.028 5.388 5.388 0 0 1-.726-.145c-.013-.004-.027-.007-.04-.01-.366-.08-1.579.52-1.996.671a17.586 17.586 0 0 1-1.874.551z" />
                                        </svg>
                                    </div>

                                    <span className="text-foreground/80 group-hover:text-foreground truncate text-sm font-medium transition-colors flex-1 select-none">
                                        {conversation.title || `Chat from ${new Date(conversation.created_at).toLocaleDateString()}`}
                                    </span>

                                    {/* Three dots menu button */}
                                    <button
                                        onClick={(e) => toggleMenu(e, conversation.id)}
                                        className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-white/10 rounded-lg text-gray-400 hover:text-white transition-all duration-200"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                            <path d="M3 9.5a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3zm5 0a1.5 1.5 0 1 1 0-3 1.5 1.5 0 0 1 0 3z" />
                                        </svg>
                                    </button>
                                </div>

                                {/* Dropdown Menu */}
                                {menuOpenId === conversation.id && (
                                    <div
                                        ref={menuRef}
                                        className="absolute right-0 top-10 w-36 bg-[#1a1f2e] border border-gray-700 rounded-xl shadow-2xl z-50 overflow-hidden backdrop-blur-sm"
                                        style={{ boxShadow: '0 4px 20px rgba(0,0,0,0.5)' }}
                                    >
                                        <button
                                            onClick={(e) => handleDelete(e, conversation.id)}
                                            className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:text-red-300 hover:bg-red-500/10 flex items-center gap-2 transition-colors"
                                        >
                                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16">
                                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
                                                <path fillRule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
                                            </svg>
                                            Delete Chat
                                        </button>
                                    </div>
                                )}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <div className="text-center py-8 px-4 opacity-50">
                        <p className="text-gray-500 text-sm mb-2">No chats yet</p>
                        <p className="text-xs text-gray-600">Start a new conversation to get help with your tasks.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Sidebar;
