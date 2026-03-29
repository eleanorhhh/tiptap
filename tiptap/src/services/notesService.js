// src/services/notesService.js
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const fetchNotes = async () => {
    try {
        // 將 /get_all_notes/ 改為後端 urls.py 設定的 /api/load_all/
        const response = await axios.get(`${API_BASE_URL}/api/load_all/`);
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
        // 將 /save_note/ 改為後端 urls.py 設定的 /api/save/
        const response = await axios.post(`${API_BASE_URL}/api/save/`, {
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
        // 將 /delete_note/${id}/ 改為後端 urls.py 設定的 /api/delete/${id}/
        const response = await axios.delete(`${API_BASE_URL}/api/delete/${id}/`);
        if (response.data.status === 'success') {
            return true;
        }
    } catch (error) {
        console.error("刪除失敗", error);
        throw error;
    }
};