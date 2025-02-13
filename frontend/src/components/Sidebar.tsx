import React from 'react';
import { MessageSquarePlus, MessagesSquare, LogOut } from 'lucide-react';
import { Chat } from '../types';

interface SidebarProps {
  chats: Chat[];
  activeChat: Chat | null;
  onNewChat: () => void;
  onSelectChat: (chat: Chat) => void;
  user: any;
  onLogout: () => void;
}

export function Sidebar({ chats, activeChat, onNewChat, onSelectChat, user, onLogout }: SidebarProps) {
  return (
    <div className="w-64 bg-gray-900 text-white h-screen flex flex-col">
      <div className="p-4 border-b border-gray-800">
        <div className="flex items-center gap-3 mb-4">
          <img 
            src={user.photoURL} 
            alt={user.displayName} 
            className="w-8 h-8 rounded-full"
          />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">{user.displayName}</p>
            <p className="text-xs text-gray-400 truncate">{user.email}</p>
          </div>
          <button
            onClick={onLogout}
            className="p-1.5 hover:bg-gray-800 rounded-lg transition-colors"
            title="Sign out"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-2 px-4 py-2 rounded-lg bg-teal-600 hover:bg-teal-700 transition-colors"
        >
          <MessageSquarePlus className="w-5 h-5" />
          <span>New Chat</span>
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        {chats.map((chat) => (
          <button
            key={chat.id}
            onClick={() => onSelectChat(chat)}
            className={`w-full text-left px-4 py-3 flex items-center gap-2 hover:bg-gray-800 transition-colors
              ${activeChat?.id === chat.id ? 'bg-gray-800' : ''}`}
          >
            <MessagesSquare className="w-5 h-5 text-gray-400" />
            <span className="truncate">{chat.title}</span>
          </button>
        ))}
      </div>
    </div>
  );
}