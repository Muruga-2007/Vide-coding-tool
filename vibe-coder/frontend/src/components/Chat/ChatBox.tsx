import React, { useState } from 'react';
import { chatService } from '../../services/api';
import { Send, Bot, User } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

const ChatBox: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        { role: 'assistant', content: 'Hello! I am Vibe Coder. How can I help you today?' }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg: Message = { role: 'user', content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput('');
        setIsLoading(true);

        try {
            // Pass project path if we have one selected (hardcoded for MVP)
            const data = await chatService.query(input, 'd:\\New folder\\Vide-Coder---testing');
            const aiMsg: Message = { role: 'assistant', content: data.response };
            setMessages(prev => [...prev, aiMsg]);
        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'assistant', content: 'Error connecting to AI.' }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-full bg-card border-l border-border">
            <div className="p-4 border-b border-border font-semibold flex items-center gap-2">
                <Bot className="w-5 h-5 text-primary" />
                AI Assistant
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((msg, idx) => (
                    <div key={idx} className={twMerge(clsx(
                        "flex gap-3 text-sm p-3 rounded-lg max-w-[90%]",
                        msg.role === 'user' ? "ml-auto bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"
                    ))}>
                        <div className="mt-1 shrink-0">
                            {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                        </div>
                        <div className="whitespace-pre-wrap">{msg.content}</div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex gap-3 text-sm p-3 rounded-lg bg-muted text-muted-foreground w-max">
                        <Bot size={16} className="mt-1 animate-pulse" />
                        <span className="italic">Thinking...</span>
                    </div>
                )}
            </div>

            <div className="p-4 border-t border-border mt-auto">
                <div className="flex gap-2">
                    <input
                        className="flex-1 bg-background border border-input rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-ring"
                        placeholder="Ask AI to edit code..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                    />
                    <button
                        onClick={handleSend}
                        disabled={isLoading}
                        className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:opacity-90 disabled:opacity-50"
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatBox;
