import React from 'react';
import { Bot, User } from 'lucide-react';
import { Message } from '../types';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === 'assistant';
  
  return (
    <div className={`py-6 ${isAssistant ? 'bg-gray-50' : ''}`}>
      <div className="max-w-3xl mx-auto flex gap-6 px-4">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 
          ${isAssistant ? 'bg-teal-600' : 'bg-blue-600'}`}>
          {isAssistant ? (
            <Bot className="w-5 h-5 text-white" />
          ) : (
            <User className="w-5 h-5 text-white" />
          )}
        </div>
        <div className="flex-1 space-y-2">
          <p className="font-medium text-sm text-gray-500">
            {isAssistant ? 'Statik' : 'You'}
          </p>
          <div className="prose prose-slate max-w-none">
            {message.content}
          </div>
        </div>
      </div>
    </div>
  );
}