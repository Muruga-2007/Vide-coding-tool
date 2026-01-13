import React from 'react';
import { Files, Search, Settings, ArrowLeft } from 'lucide-react';

interface SidebarProps {
    activeFile: string;
    onFileSelect: (file: string) => void;
    onBack: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeFile, onFileSelect, onBack }) => {
    return (
        <div style={{ display: 'flex', height: '100%' }}>
            {/* Activity Bar */}
            <div style={{
                width: '50px',
                backgroundColor: '#333333',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                paddingTop: '1rem',
                borderRight: '1px solid #2b2b2b',
                justifyContent: 'space-between'
            }}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', alignItems: 'center' }}>
                    <Files size={24} color={activeFile ? '#fff' : '#858585'} />
                    <Search size={24} color="#858585" />
                </div>

                <div style={{ marginBottom: '1rem', display: 'flex', flexDirection: 'column', gap: '1.5rem', alignItems: 'center' }}>
                    <Settings size={24} color="#858585" />
                    <ArrowLeft
                        size={24}
                        color="#858585"
                        style={{ cursor: 'pointer' }}
                        onClick={onBack}
                        title="Back to Home"
                    />
                </div>
            </div>

            {/* Explorer Panel */}
            <div style={{ width: '250px', backgroundColor: '#252526', padding: '0.5rem' }}>
                <div style={{ fontSize: '0.8rem', fontWeight: 'bold', padding: '0.5rem', color: '#bbbbbb' }}>EXPLORER</div>

                <div style={{ marginTop: '0.5rem' }}>
                    <div style={{ padding: '0.25rem 0.5rem', fontWeight: 'bold', fontSize: '0.8rem', color: '#cccccc' }}>
                        V PROJECT REPO
                    </div>
                    {/* Mock File Tree */}
                    <div style={{ marginLeft: '1rem', display: 'flex', flexDirection: 'column', gap: '2px' }}>
                        {['App.tsx', 'index.css', 'components/Hero.tsx', 'components/Features.tsx', 'utils/api.ts'].map(file => (
                            <div
                                key={file}
                                onClick={() => onFileSelect(file)}
                                style={{
                                    cursor: 'pointer',
                                    padding: '3px 5px',
                                    fontSize: '0.9rem',
                                    color: activeFile === file ? '#fff' : '#969696',
                                    backgroundColor: activeFile === file ? '#37373d' : 'transparent',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '6px'
                                }}
                            >
                                <span style={{ color: file.endsWith('tsx') ? '#4d9bb0' : '#dcb67d' }}>
                                    {/* Icon placeholder */}
                                    {file.endsWith('tsx') ? '⚛️' : '#'}
                                </span>
                                {file.split('/').pop()}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
