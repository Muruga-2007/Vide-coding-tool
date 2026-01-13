import React, { useState, useEffect } from 'react';
import { GenerationResult } from '../../types';

interface TerminalProps {
    result: GenerationResult | null;
    loading: boolean;
    error: string | null;
}

const Terminal: React.FC<TerminalProps> = ({ result, loading, error }) => {
    const [logs, setLogs] = useState<string[]>([]);

    useEffect(() => {
        setLogs([
            'System ready.',
            '> Waiting for input...'
        ]);
    }, []);

    useEffect(() => {
        if (loading) {
            setLogs(prev => [...prev, '> Starting agent workflow...', '> Initializing Planner, Copywriter, and Coder...']);
        }
    }, [loading]);

    useEffect(() => {
        if (result) {
            setLogs(prev => [...prev,
                '> Planner Agent finished.',
                '> Copywriter Agent finished.',
                '> Code Generator Agent finished.',
                '> Aggregating results...',
                '> Build successful.'
            ]);
        }
    }, [result]);

    useEffect(() => {
        if (error) {
            setLogs(prev => [...prev, `> Error: ${error}`]);
        }
    }, [error]);

    return (
        <div style={{ height: '100%', backgroundColor: '#1e1e1e', display: 'flex', flexDirection: 'column' }}>
            <div style={{
                height: '35px',
                borderBottom: '1px solid #2b2b2b',
                display: 'flex',
                alignItems: 'center',
                padding: '0 1rem',
                gap: '2rem',
                fontSize: '0.8rem',
                textTransform: 'uppercase',
                color: '#969696'
            }}>
                <span style={{ color: '#fff', borderBottom: '1px solid #007acc', height: '100%', display: 'flex', alignItems: 'center' }}>Terminal</span>
                <span>Output</span>
                <span>Problems</span>
                <span>Debug Console</span>
            </div>

            <div style={{
                flex: 1,
                padding: '0.5rem 1rem',
                overflowY: 'auto',
                fontFamily: 'Consolas, monospace',
                fontSize: '0.9rem',
                color: '#cccccc'
            }}>
                {logs.map((log, i) => (
                    <div key={i} style={{ marginBottom: '4px' }}>
                        {log}
                    </div>
                ))}
                {loading && (
                    <div style={{ color: '#007acc' }}>Compiling agents...</div>
                )}
            </div>
        </div>
    );
};

export default Terminal;
