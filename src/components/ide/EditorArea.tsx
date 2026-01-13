import React, { useState } from 'react';
import { GenerationResult } from '../../types';
import CodePreview from '../CodePreview';

// Note: We're reusing CodePreview but wrapping it in an IDE-style tab system
interface EditorAreaProps {
    result: GenerationResult | null;
    loading: boolean;
}

type Tab = 'final' | 'code' | 'plan' | 'copy';

const EditorArea: React.FC<EditorAreaProps> = ({ result, loading }) => {
    const [activeTab, setActiveTab] = useState<Tab>('final');

    if (loading) {
        return (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#858585' }}>
                <div style={{ textAlign: 'center' }}>
                    <div className="spinner" style={{ marginBottom: '1rem' }}>⚡</div>
                    <div>Generating codebase...</div>
                </div>
            </div>
        );
    }

    if (!result) {
        return (
            <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#333' }}>
                <div style={{
                    fontSize: '5rem',
                    opacity: 0.05,
                    fontWeight: 'bold',
                    userSelect: 'none'
                }}>
                    VIBE
                </div>
            </div>
        );
    }

    return (
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: '#1e1e1e' }}>
            {/* Tabs */}
            <div style={{ display: 'flex', backgroundColor: '#252526', height: '35px', alignItems: 'center' }}>
                {[
                    { id: 'final', label: 'Preview' },
                    { id: 'code', label: 'Source Code' },
                    { id: 'plan', label: 'Implementation Plan.md' },
                    { id: 'copy', label: 'Copywriting.txt' }
                ].map(tab => (
                    <div
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id as Tab)}
                        style={{
                            padding: '0 15px',
                            height: '100%',
                            display: 'flex',
                            alignItems: 'center',
                            fontSize: '0.9rem',
                            cursor: 'pointer',
                            backgroundColor: activeTab === tab.id ? '#1e1e1e' : 'transparent',
                            color: activeTab === tab.id ? '#fff' : '#969696',
                            borderTop: activeTab === tab.id ? '1px solid #007acc' : '1px solid transparent',
                            borderRight: '1px solid #2b2b2b'
                        }}
                    >
                        {tab.label}
                    </div>
                ))}
            </div>

            {/* Content */}
            <div style={{ flex: 1, overflow: 'auto', position: 'relative' }}>
                {activeTab === 'final' && (
                    <CodePreview code={result.final_code} summary={result.summary} improvements={result.improvements} />
                )}

                {activeTab === 'code' && (
                    <pre style={{ margin: 0, padding: '1rem', overflow: 'auto', fontSize: '0.9rem', fontFamily: 'Consolas, monospace' }}>
                        {result.code}
                    </pre>
                )}

                {activeTab === 'plan' && (
                    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontSize: '0.9rem', lineHeight: '1.6' }}>
                        <h3>Planner Output</h3>
                        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>{result.plan}</pre>
                    </div>
                )}

                {activeTab === 'copy' && (
                    <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto', fontSize: '0.9rem', lineHeight: '1.6' }}>
                        <h3>Copywriter Output</h3>
                        <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>{result.copywriting}</pre>
                    </div>
                )}
            </div>
        </div>
    );
};

export default EditorArea;
