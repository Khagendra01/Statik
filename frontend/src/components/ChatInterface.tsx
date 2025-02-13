import React from 'react';
import { Chat, Message } from '../types';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { Sidebar } from './Sidebar';
import { LogOut } from 'lucide-react';

interface ChatInterfaceProps {
  user: any;
  onLogout: () => void;
}

function ChatInterface({ user, onLogout }: ChatInterfaceProps) {
  const [chats, setChats] = React.useState<Chat[]>([]);
  const [activeChat, setActiveChat] = React.useState<Chat | null>(null);

  const createNewChat = () => {
    const newChat: Chat = {
      id: crypto.randomUUID(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date(),
    };
    setChats([newChat, ...chats]);
    setActiveChat(newChat);
  };

  const handleSendMessage = (content: string) => {
    if (!activeChat) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      content: 'I am Statik, your AI assistant. How can I help you today?',
      role: 'assistant',
      timestamp: new Date(),
    };

    const updatedChat = {
      ...activeChat,
      messages: [...activeChat.messages, userMessage, assistantMessage],
      title: activeChat.messages.length === 0 ? content : activeChat.title,
    };

    setChats(chats.map(chat => 
      chat.id === activeChat.id ? updatedChat : chat
    ));
    setActiveChat(updatedChat);
  };

  return (
    <div className="flex h-screen bg-white">
      <Sidebar
        chats={chats}
        activeChat={activeChat}
        onNewChat={createNewChat}
        onSelectChat={setActiveChat}
        user={user}
        onLogout={onLogout}
      />
      
      <main className="flex-1 flex flex-col">
        {activeChat ? (
          <>
            <div className="flex-1 overflow-y-auto">
              {activeChat.messages.map((message) => (
                <ChatMessage key={message.id} message={message} />
              ))}
            </div>
            <ChatInput onSend={handleSendMessage} />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center space-y-4">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-teal-500 to-blue-500 bg-clip-text text-transparent">
                Welcome to Statik
              </h1>
              <p className="text-gray-500">Start a new chat or select an existing conversation</p>
              <button
                onClick={createNewChat}
                className="px-4 py-2 rounded-lg bg-teal-600 text-white hover:bg-teal-700 transition-colors"
              >
                Start New Chat
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default ChatInterface;