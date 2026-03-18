<template>
  <div class="slash-menu" v-if="items.length">
    <ul class="menu-list">
      <li
        v-for="(item, index) in items"
        :key="index"
        :class="{ 'is-selected': index === selectedIndex }"
        @click="selectItem(index)"
      >
        <span class="icon">{{ getIcon(item.title) }}</span>
        {{ item.title }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  items: Array,    // 從 WorkSpace 傳進來的清單
  command: Function, // 點擊後要執行的動作
})

const selectedIndex = ref(0)

// 當使用者繼續打字過濾清單時，重置選中位置到第一個
watch(() => props.items, () => {
  selectedIndex.value = 0
})

// 處理鍵盤邏輯（這就是之前報錯的 onKeyDown）
const onKeyDown = ({ event }) => {
  if (event.key === 'ArrowUp') {
    selectedIndex.value = (selectedIndex.value + props.items.length - 1) % props.items.length
    return true
  }
  if (event.key === 'ArrowDown') {
    selectedIndex.value = (selectedIndex.value + 1) % props.items.length
    return true
  }
  if (event.key === 'Enter') {
    selectItem(selectedIndex.value)
    return true
  }
  return false
}

const selectItem = (index) => {
  const item = props.items[index]
  if (item) {
    props.command(item) // 執行 Tiptap 的指令
  }
}

// 根據標題給圖示（你可以自己改）
const getIcon = (title) => {
  if (title.includes('標題')) return 'H'
  if (title.includes('圖片')) return '📷'
  if (title.includes('粗體')) return 'B'
  return '•'
}

// ⚠️ 重要：把這個方法暴露給外面，這樣 WorkSpace 才能呼叫它
defineExpose({ onKeyDown })
</script>

<style scoped>
.slash-menu {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  padding: 4px;
  min-width: 150px;
}
.menu-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.menu-list li {
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 4px;
  display: flex;
  align-items: center;
}
.icon {
  margin-right: 10px;
  width: 20px;
  text-align: center;
  color: #888;
}
.menu-list li.is-selected {
  background-color: #f1f1f1;
  color: #42b983;
}
</style>