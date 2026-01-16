import React, { useEffect, useState } from 'react';
import { fileService } from '../../services/api';
import { Folder, FileText, ChevronRight, ChevronDown, RefreshCw } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface FileNode {
    path: string;
    name: string;
    type: 'file' | 'directory';
    children?: FileNode[];
    isOpen?: boolean;
}

interface FileTreeProps {
    onFileSelect: (path: string) => void;
    rootPath?: string;
}

const FileTree: React.FC<FileTreeProps> = ({ onFileSelect, rootPath = 'd:\\New folder\\Vide-Coder---testing' }) => {
    const [files, setFiles] = useState<FileNode[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchFiles = async () => {
        setLoading(true);
        setError(null);
        try {
            const flatFiles = await fileService.list(rootPath);
            // Convert flat list to tree
            const tree = buildTree(flatFiles);
            setFiles(tree);
        } catch (err: any) {
            setError(err.message || 'Failed to load files');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFiles();
    }, [rootPath]);

    const buildTree = (flatList: any[]): FileNode[] => {
        // Simplified: Just returning flat list as children of root for now
        // A real implementation would parse paths into a tree structure
        const root: FileNode[] = [];

        // Basic grouping by top-level folders
        // For this MVP, let's just show the flat list sorted by type
        return flatList.sort((a, b) => {
            if (a.type === b.type) return a.name.localeCompare(b.name);
            return a.type === 'directory' ? -1 : 1;
        }).map(f => ({ ...f, isOpen: false }));
    };

    const toggleFolder = (node: FileNode) => {
        // In a real tree, we'd toggle isOpen
        // Since we have a flat list acting as one level for MVP:
        onFileSelect(node.path);
    };

    return (
        <div className="flex flex-col h-full bg-muted/20 text-sm">
            <div className="flex items-center justify-between p-3 border-b border-border">
                <span className="font-semibold text-muted-foreground uppercase text-xs">Files</span>
                <button onClick={fetchFiles} className="text-muted-foreground hover:text-foreground">
                    <RefreshCw size={14} className={loading ? "animate-spin" : ""} />
                </button>
            </div>

            {error && <div className="p-4 text-destructive">{error}</div>}

            <div className="flex-1 overflow-y-auto p-2">
                {files.map((node, idx) => (
                    <div
                        key={idx}
                        className="flex items-center gap-2 p-1 hover:bg-muted/50 rounded cursor-pointer truncate"
                        onClick={() => node.type === 'file' ? onFileSelect(node.path) : null}
                    >
                        {node.type === 'directory' ? (
                            <Folder size={16} className="text-blue-400 shrink-0" />
                        ) : (
                            <FileText size={16} className="text-gray-400 shrink-0" />
                        )}
                        <span className="truncate">{node.name}</span>
                    </div>
                ))}
                {files.length === 0 && !loading && (
                    <div className="text-muted-foreground p-4 text-center italic">No files found</div>
                )}
            </div>
        </div>
    );
};

export default FileTree;
