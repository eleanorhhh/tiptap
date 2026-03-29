
```markdown
# Notion-like Editor (Tiptap + Django + Vue 3)

這是一個具備豐富文字編輯功能的類 Notion 筆記應用程式。前端採用 Vue 3 與 Vite 建構，並整合 Tiptap 編輯器；後端則使用 Django 框架提供 API 服務，支援筆記的完整 CRUD (新增、讀取、更新、刪除) 功能。

## 🛠️ 技術堆疊

### 前端 (Frontend)
* **核心框架**: Vue 3
* **建置工具**: Vite
* **編輯器套件**: Tiptap (`@tiptap/vue-3`, `@tiptap/starter-kit`)
* **編輯器擴充功能**: 支援程式碼區塊 (code-block)、螢光筆 (highlight)、圖片 (image)、佔位符 (placeholder) 與待辦清單 (task-list) 等功能
* **HTTP 客戶端**: Axios

### 後端 (Backend)
* **核心框架**: Django
* **資料模型**: 
    * 使用 UUID 作為筆記的主鍵 (`id`)，提升安全性與前端整合的便利性
    * 直接儲存 Tiptap 產生的整包 JSON 格式內容 (`content_json`)
    * 自動記錄筆記的建立時間 (`created_at`) 與更新時間 (`updated_at`)

## 🔌 API 路由與服務設計

前端透過 `notesService.js` 與運行在 `http://127.0.0.1:8000` 的 Django 伺服器進行溝通。

* **讀取所有筆記**:
    * 前端端點: `GET /api/load_all/`
    * 後端對應: `load_all/`
* **儲存/新增筆記**:
    * 前端端點: `POST /api/save/`
    * 後端對應: `save/`
* **刪除筆記**:
    * 前端端點: `DELETE /api/delete/${id}/`
    * 後端對應: `delete_note/<str:id>/`

## 🚀 本地開發與啟動指南

### 前端環境設定 (tiptap 目錄)
請確保你的 Node.js 版本符合 `>=22.12.0` 或 `^20.19.0`。

1. 進入前端專案目錄並安裝依賴：
```bash
npm install
```
2. 啟動 Vite 開發伺服器：
```bash
npm run dev
```


### 後端環境設定
1. 確保已安裝 Python 與 Django。
2. 在根目錄進行資料庫遷移 (Migrations)：
```bash
python manage.py makemigrations
python manage.py migrate
```
3. 啟動 Django 開發伺服器：
```bash
python manage.py runserver
```
```
