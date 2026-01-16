import React, { useState } from 'react';
import CodeEditor from '../editor/CodeEditor';
import ChatBox from '../components/Chat/ChatBox';
import FileTree from '../components/FileExplorer/FileTree';
import TerminalView from '../components/Terminal/TerminalView';

const Workspace: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<string | null>(null);

    const handleFileSelect = (path: string) => {
        console.log("Selected:", path);
        setSelectedFile(path);
        // TODO: Load file content into editor
    };

    return (
        <div className="h-screen w-full flex flex-col bg-background text-foreground overflow-hidden">
            <div className="flex-1 flex overflow-hidden">
                {/* Sidebar (File Explorer) */}
                <div className="w-64 border-r border-border flex flex-col hidden md:flex">
                    <FileTree onFileSelect={handleFileSelect} />
                </div>

                {/* Main Editor Area */}
                <div className="flex-1 flex flex-col min-w-0">
                    <div className="h-12 border-b border-border flex items-center px-4 bg-card">
                        <span className="text-sm font-medium">{selectedFile || 'No file selected'}</span>
                    </div>
                    <div className="flex-1 relative">
                        <CodeEditor />
                    </div>
                </div>

                {/* Right Panel (AI Chat) */}
                <div className="w-96 border-l border-border bg-card">
                    <ChatBox />
                </div>
            </div>

            {/* Terminal Panel */}
            <div className="h-48 border-t border-border">
                <TerminalView />
            </div>
        </div>
    );
};

export default Workspace;
