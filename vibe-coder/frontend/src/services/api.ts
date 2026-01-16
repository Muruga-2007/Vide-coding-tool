const API_BASE_URL = 'http://localhost:8000/api/v1';

export const chatService = {
    async query(message: string, projectPath?: string, history?: any[]) {
        const response = await fetch(`${API_BASE_URL}/chat/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                project_path: projectPath,
                history,
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to send message');
        }

        return response.json();
    }
};

export const fileService = {
    async indexProject(path: string) {
        const response = await fetch(`${API_BASE_URL}/files/index`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ path }),
        });

        if (!response.ok) {
            throw new Error('Failed to index project');
        }
        return response.json();
    },

    async list(path: string) {
        const params = new URLSearchParams({ path });
        const response = await fetch(`${API_BASE_URL}/files/list?${params}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Failed to list files');
        }
        return response.json();
    }
};

export const terminalService = {
    async run(command: string, cwd?: string) {
        const response = await fetch(`${API_BASE_URL}/terminal/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ command, cwd }),
        });

        if (!response.ok) {
            throw new Error('Failed to run command');
        }
        return response.json();
    }
};
