<script setup>
import SideBar from './component/SideBar.vue';
import WorkSpace from './component/WorkSpace.vue';
</script>
<template>
<div class="main-container">
<SideBar/>
<WorkSpace/>
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