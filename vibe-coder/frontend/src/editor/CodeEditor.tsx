import React from 'react';
import Editor, { OnMount } from '@monaco-editor/react';

interface CodeEditorProps {
    initialValue?: string;
    language?: string;
    onChange?: (value: string | undefined) => void;
    theme?: 'vs-dark' | 'light';
}

const CodeEditor: React.FC<CodeEditorProps> = ({
    initialValue = '// Start coding...',
    language = 'python',
    onChange,
    theme = 'vs-dark'
}) => {
    const handleEditorDidMount: OnMount = (editor, monaco) => {
        // Enable minimap, etc.
        editor.updateOptions({
            minimap: { enabled: true },
            fontSize: 14,
            scrollBeyondLastLine: false,
        });
    };

    return (
        <div className="h-full w-full overflow-hidden border border-border rounded-md">
            <Editor
                height="100%"
                defaultLanguage={language}
                defaultValue={initialValue}
                theme={theme}
                onMount={handleEditorDidMount}
                onChange={onChange}
                options={{
                    automaticLayout: true,
                    padding: { top: 16 }
                }}
            />
        </div>
    );
};

export default CodeEditor;
