const BASE_URL = '/api';

let savedInitData = '';

export const api = {
    login: async (initData: string) => {
        savedInitData = initData;
        const res = await fetch(`${BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ initData })
        });
        if (!res.ok) throw new Error('Login failed');
        return res.json();
    },
    getQuestions: async () => {
        const res = await fetch(`${BASE_URL}/questions`, {
            headers: { 'Authorization': `Bearer ${savedInitData}` }
        });
        if (!res.ok) throw new Error('Failed to fetch questions');
        return res.json();
    },
    submitAnswer: async (questionId: string, selectedOption: string) => {
        const res = await fetch(`${BASE_URL}/answer`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${savedInitData}`
            },
            body: JSON.stringify({ question_id: questionId, selected_option: selectedOption })
        });
        if (!res.ok) throw new Error('Submit failed');
        return res.json();
    }
};
