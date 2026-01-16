import React, { useState, useRef, useEffect } from 'react';
import { terminalService } from '../../services/api';
import { Terminal as TerminalIcon } from 'lucide-react';

const TerminalView: React.FC = () => {
    const [output, setOutput] = useState<string>('Vibe Coder Terminal v1.0\n');
    const [input, setInput] = useState('');
    const [cwd, setCwd] = useState('d:\\New folder\\Vide-Coder---testing'); // Default for MVP
    const [isLoading, setIsLoading] = useState(false);
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [output]);

    const handleKeyDown = async (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            if (!input.trim()) return;

            const command = input;
            setInput('');
            setOutput(prev => prev + `\n$ ${command}\n`);
            setIsLoading(true);

            try {
                const res = await terminalService.run(command, cwd);
                if (res.stdout) setOutput(prev => prev + res.stdout + '\n');
                if (res.stderr) setOutput(prev => prev + res.stderr + '\n');
                if (res.return_code !== 0) setOutput(prev => prev + `Exit code: ${res.return_code}\n`);
            } catch (err: any) {
                setOutput(prev => prev + `Error: ${err.message}\n`);
            } finally {
                setIsLoading(false);
            }
        }
    };

    return (
        <div className="flex flex-col h-full bg-black text-white font-mono text-sm">
            <div className="flex items-center px-4 py-2 border-b border-gray-700 bg-gray-900">
                <TerminalIcon size={14} className="mr-2" />
                <span>Terminal</span>
            </div>

            <div className="flex-1 overflow-y-auto p-4 whitespace-pre-wrap">
                {output}
                <div ref={bottomRef} />
            </div>

            <div className="p-2 border-t border-gray-700 flex gap-2 items-center bg-gray-900">
                <span className="text-green-500">$</span>
                <input
                    className="flex-1 bg-transparent focus:outline-none"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    autoFocus
                    disabled={isLoading}
                />
            </div>
        </div>
    );
};

export default TerminalView;
