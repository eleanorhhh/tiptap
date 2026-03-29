<script setup>
import {ref , onMounted } from 'vue'
import axios from 'axios';

const notes = ref([]);
const isCollapsed = ref(false);
const emit = defineEmits(['select-note']);

//定義漢堡按鈕的收和狀態
const toggleSidebar =() =>{
    isCollapsed.value = !isCollapsed.value;
}
//獲取所有的筆記（對應get_all_notes)
const fetchNotes = async() =>{
    try{
        const response = await axios.get('http://127.0.0.1:8000/api/load_all/')
        if (response.data.status === 'success'){
            notes.value = response.data.notes;
        }
    } catch(error){
        console.error("讀取筆記失敗",error);
    }
};

//新增筆記（對應save_note,不帶id視為create）
const createNewNote = async () => {
  const baseTitle = "新筆記";
  let finalTitle = baseTitle;
  let counter = 1;

  // 檢查名稱是否重複的邏輯
  // 假設 notes.value 是目前所有的筆記列表
  const existingTitles = notes.value.map(n => n.title);

  while (existingTitles.includes(finalTitle)) {
    finalTitle = `${baseTitle} (${counter})`;
    counter++;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/save/', {
      title: finalTitle, // 使用計算後的名稱
      body_content: ''
    });
    
    if (response.data.status === 'success') {
      await fetchNotes();
      const newNote = notes.value.find(n => n.id === response.data.id);
      if (newNote) {
        selectNote(newNote);
      }
    }
  } catch (error) {
    console.error("建立失敗", error);
  }
};

const deleteNote = async(id) =>{
    if(!confirm('確定要刪除嗎？')) return;
    try{
        // 注意：這裡改成反引號 (`) 才能正確解析變數 ${id}
        const response = await axios.delete(`http://127.0.0.1:8000/delete_note/${id}/`);
        if (response.data.status === 'success'){
            notes.value = notes.value.filter(n => n.id !==id);
        }

    }catch(error){
        console.error("刪除失敗",error);
    }
};

const currentNoteId = ref(null);

const selectNote = (note) => {
  currentNoteId.value = note.id; // 記錄選中的 ID
  emit('select-note', note);
};


onMounted(fetchNotes);
defineExpose({ fetchNotes });


</script>
<template>
    <div class="SiderBar">
    <button @click="toggleSidebar" class="menu-btn">
        ☰
    </button>
    <div :class="['sidebar',{'collapsed': isCollapsed}]">
        <div clas="sidebar-inner" v-show="!isCollapsed">
            <button @click="createNewNote" class="add-note-btn">
                <span>+</span>新增筆記
            </button>
            <h3 class="section-title">歷史頁面</h3>
            <div id="history-list">
            <div 
            v-for="note in notes" 
            :key="note.id" 
            class="note-item"
            :class="{ 'active': currentNoteId === note.id }"
            @click="selectNote(note)"
            >                      
            <h4>{{ note.title || '未命名筆記' }} </h4>      
            <button class="delete-btn" @click.stop="deleteNote(note.id)">x</button>      
        </div>

            </div>
        </div>
    </div>
    </div>

</template>
<style scoped >
/* 側邊欄佈局結構 */
   .menu-btn {
    position: fixed;
    top: 15px;
    left: 15px;
    z-index: 1000;
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: 24px;
    color: #37352f;
}

.sidebar {
    width: 260px;
    height: 100vh;
    background-color: #f7f6f3;
    border-right: 1px solid #edece9;
    padding: 60px 12px 20px 12px;
    transition: width 0.3s ease, padding 0.3s ease;
    overflow-x: hidden; /* 防止收合時文字溢出 */
    box-sizing: border-box; /* 確保 100vh 加上 padding 後不會超出畫面 */
}

/* 當 isCollapsed 為 true 時套用的樣式 */
.sidebar.collapsed {
    width: 0;
    padding-left: 0;
    padding-right: 0;
    border-right: none;
}

.sidebar-inner {
    width: 236px; /* 固定的內部寬度，避免縮放時內容亂跳 */
}

/* 之前建議的按鈕與清單樣式... */
.add-note-btn {
    background: #ffffff;
    border: 1px solid #ddd;
    padding: 8px;
    border-radius: 6px;
    margin-bottom: 20px;
    width: 100%;
    cursor: pointer;
    font-weight: bold;
}
.section-title{
    font-size: 12px; 
    color: #91918e; 
    margin: 0 0 15px 10px; 
    text-transform: uppercase; 
    letter-spacing: 0.5px;
}
.note-item {
  display: flex;
  justify-content: space-between; /* 讓標題靠左，按鈕靠右 */
  align-items: center; /* 讓兩者垂直置中對齊 */
  
  /* 這些保留你原本的設定 */
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
}

.note-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

/* 點擊時的縮放動畫 */
.note-item:active {
  transform: scale(0.97);
}

/* 選中後的樣式 */
.note-item.active {
  background-color: #e3f2fd;
  color: #1976d2;
  font-weight: bold;
  border-left: 4px solid #1976d2;
}
/* 針對標題的設定 */
.note-title {
  margin: 0; /* 【關鍵】清除 h4 預設的上下邊距，才不會撐壞排版或換行 */
  flex: 1; /* 讓標題佔滿左側剩下的空間 */
  
  /* 如果標題太長，變成 ... 而不會把叉叉擠到外面 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-align: left;
}

/* 針對叉叉按鈕的設定 */
.delete-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  margin-left: 8px; /* 跟左邊的標題保持一點距離 */
  color: #999; /* 預設顏色 */
  display: none; /* 如果你希望 hover 才顯示，就加上這行 */
}

/* 滑鼠移過去才顯示叉叉（依你的需求決定要不要加） */
.note-item:hover .delete-btn {
  display: block;
}

.delete-btn:hover {
  color: #ff4d4f; /* 滑鼠移到叉叉上變紅色 */
}

.delete-btn {
  display: none; /* 預設隱藏 */
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 14px;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

/* 當滑鼠移到筆記項目 (note-item) 上時，才顯示刪除按鈕 */
.note-item:hover .delete-btn {
  display: block;
}

</style>