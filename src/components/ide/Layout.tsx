import React, { useState } from 'react';
import Sidebar from './Sidebar';
import EditorArea from './EditorArea';
import Terminal from './Terminal';
import ChatPanel from './ChatPanel';
import { GenerationResult } from '../../types';

interface LayoutProps {
    onBack: () => void;
}

const Layout: React.FC<LayoutProps> = ({ onBack }) => {
    // State
    const [result, setResult] = useState<GenerationResult | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [activeFile, setActiveFile] = useState<string>('App.tsx');

    // Handler for generation
    const handleGenerate = async (prompt: string) => {
        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await fetch('http://localhost:8000/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) throw new Error('Generation failed');
            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'An error occurred');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{
            display: 'flex',
            height: '100vh',
            width: '100vw',
            backgroundColor: '#1e1e1e',
            color: '#ccccc7',
            overflow: 'hidden',
            fontFamily: 'Consolas, "Courier New", monospace'
        }}>
            {/* Left Sidebar (Activity Bar + Explorer) */}
            <Sidebar activeFile={activeFile} onFileSelect={setActiveFile} onBack={onBack} />

            {/* Main Content Area */}
            <div style={{ display: 'flex', flexDirection: 'column', flex: 1, borderLeft: '1px solid #2b2b2b' }}>

                {/* Editor & Preview */}
                <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
                    <EditorArea result={result} loading={loading} />

                    {/* Right Panel: Chat/Agents */}
                    <div style={{ width: '350px', borderLeft: '1px solid #2b2b2b', display: 'flex', flexDirection: 'column' }}>
                        <ChatPanel onGenerate={handleGenerate} loading={loading} error={error} />
                    </div>
                </div>

                {/* Bottom Panel: Terminal */}
                <div style={{ height: '200px', borderTop: '1px solid #2b2b2b' }}>
                    <Terminal result={result} loading={loading} error={error} />
                </div>
            </div>
        </div>
    );
};

export default Layout;
