<script setup>
import { ref } from 'vue';
import SideBar from './component/SideBar.vue';
import WorkSpace from './component/WorkSpace.vue';

// 記住目前選中的筆記
const currentNote = ref(null);
// 取得 SideBar 元件的參考，用來呼叫它重新讀取筆記
const sidebarRef = ref(null);

// 當在 SideBar 點擊筆記時觸發
const handleSelectNote = (note) => {
  currentNote.value = note;
};

// 當在 WorkSpace 儲存成功時觸發，通知 SideBar 重新抓取資料
const handleNoteSaved = () => {
  if (sidebarRef.value) {
    sidebarRef.value.fetchNotes();
  }
};
</script>

<template>
<div class="main-container">
  <SideBar ref="sidebarRef" @select-note="handleSelectNote" />
  
  <WorkSpace :currentNote="currentNote" @note-saved="handleNoteSaved" />
</div>
</template>
<style>
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}

.main-container {
  display: flex; /* 讓側邊欄跟內容橫向並排 */
  width: 100vw;
  height: 100vh;
  overflow: hidden; /* 防止出現奇怪的捲軸 */
}

.content-area {
  flex-grow: 1; /* 自動吃掉剩下的所有寬度 */
  overflow-y: auto; /* 只有內容區可以捲動 */
  background-color: #ffffff;
}
</style>