import React, { useState, useEffect } from 'react';
import { Send, Sparkles } from 'lucide-react';

interface ChatPanelProps {
    onGenerate: (prompt: string) => void;
    loading: boolean;
    error: string | null;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ onGenerate, loading, error }) => {
    const [input, setInput] = useState('');
    const [history, setHistory] = useState<{ role: 'user' | 'agent', text: string }[]>([]);

    const handleSubmit = () => {
        if (!input.trim() || loading) return;

        // Add user message
        const newHistory = [...history, { role: 'user' as const, text: input }];
        setHistory(newHistory);

        // Trigger generation
        onGenerate(input);
        setInput('');
    };

    // Auto-scroll to bottom of chat could go here

    // Add agent response when loading starts/stops (simulated)
    useEffect(() => {
        if (loading) {
            setHistory(prev => [...prev, { role: 'agent', text: 'Working on it...' }]);
        } else if (history.length > 0 && history[history.length - 1].text === 'Working on it...') {
            // Replace "Working on it" or append done? 
            // For now we just leave it, maybe update it.
        }
    }, [loading]);

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%', backgroundColor: '#252526' }}>
            <div style={{ height: '40px', padding: '10px', borderBottom: '1px solid #3c3c3c', fontSize: '0.9rem', fontWeight: 'bold' }}>
                AI ASSISTANT
            </div>

            {/* Chat History */}
            <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {history.length === 0 && (
                    <div style={{ color: '#858585', textAlign: 'center', marginTop: '2rem', fontSize: '0.9rem' }}>
                        <Sparkles size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                        <p>Ask me to build a website.<br />Example: "Landing page for a coffee shop"</p>
                    </div>
                )}

                {history.map((msg, i) => (
                    <div key={i} style={{
                        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        backgroundColor: msg.role === 'user' ? '#0e639c' : '#3c3c3c',
                        padding: '8px 12px',
                        borderRadius: '6px',
                        maxWidth: '85%',
                        fontSize: '0.9rem',
                        lineHeight: '1.4'
                    }}>
                        {msg.text}
                    </div>
                ))}

                {error && (
                    <div style={{ color: '#f48771', padding: '0.5rem', fontSize: '0.9rem' }}>
                        Error: {error}
                    </div>
                )}
            </div>

            {/* Input Area */}
            <div style={{ padding: '1rem', borderTop: '1px solid #3c3c3c' }}>
                <div style={{
                    display: 'flex',
                    backgroundColor: '#3c3c3c',
                    borderRadius: '4px',
                    border: '1px solid #007acc'
                }}>
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSubmit();
                            }
                        }}
                        placeholder="Describe your website..."
                        style={{
                            flex: 1,
                            backgroundColor: 'transparent',
                            color: '#fff',
                            border: 'none',
                            padding: '10px',
                            outline: 'none',
                            resize: 'none',
                            fontFamily: 'inherit',
                            minHeight: '40px'
                        }}
                    />
                    <button
                        onClick={handleSubmit}
                        disabled={loading}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            color: '#fff',
                            padding: '0 10px',
                            cursor: 'pointer',
                            opacity: loading ? 0.5 : 1
                        }}
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ChatPanel;
