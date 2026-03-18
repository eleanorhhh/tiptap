// src/services/notesService.js
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const fetchNotes = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/get_all_notes/`);
        if (response.data.status === 'success') {
            return response.data.notes;
        }
    } catch (error) {
        console.error("讀取筆記失敗", error);
        throw error;
    }
};

export const createNote = async (title, body_content) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/save_note/`, {
            title,
            body_content
        });
        if (response.data.status === 'success') {
            return response.data.id;
        }
    } catch (error) {
        console.error("新增筆記失敗", error);
        throw error;
    }
};

export const deleteNote = async (id) => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/delete_note/${id}/`);
        if (response.data.status === 'success') {
            return true;
        }
    } catch (error) {
        console.error("刪除失敗", error);
        throw error;
    }
};