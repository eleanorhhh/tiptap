<script setup>
import { ref ,watch } from 'vue'
import axios from 'axios'
import { useEditor, EditorContent, VueRenderer } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import { Extension } from '@tiptap/core'
import Suggestion from '@tiptap/suggestion'
import tippy from 'tippy.js'
import 'tippy.js/dist/tippy.css'

// 匯入缺少的擴充功能
import TaskList from '@tiptap/extension-task-list'
import TaskItem from '@tiptap/extension-task-item'
import Highlight from '@tiptap/extension-highlight'
import CodeBlock from '@tiptap/extension-code-block'
import Image from '@tiptap/extension-image'

// 匯入 SlashMenuList 組件
import SlashMenuList from './SlashMenuList.vue'

// --- 定義 Toolbar 功能 ---
const toggleBold = () => editor.value.chain().focus().toggleBold().run()
const toggleHeading = () => editor.value.chain().focus().toggleHeading({ level: 1 }).run()
const toggleHighlight = () => editor.value.chain().focus().toggleHighlight().run()
const toggleTaskList = () => editor.value.chain().focus().toggleTaskList().run()
const toggleCodeBlock = () => editor.value.chain().focus().toggleCodeBlock().run()

const props = defineProps(['currentNote']) // 接收外部傳來的筆記
const emit = defineEmits(['note-saved']) // 定義要往外傳的儲存成功事件

const title = ref('')



const saveContent = async () => {
    // 檢查是否有選中筆記 (必須要有 ID 才知道要更新哪一篇)
    if (!props.currentNote || !props.currentNote.id) {
        alert("請先在左側選擇或新增一篇筆記！");
        return;
    }

    try {
        const response = await axios.post('http://127.0.0.1:8000/api/save/', {
            id: props.currentNote.id,
            title: title.value,
            body_content: editor.value.getHTML() // 抓取 Tiptap 的 HTML 內容
        });
        
        if (response.data.status === 'success') {
            alert("筆記儲存成功！");
            emit('note-saved'); // 通知 App.vue 儲存成功了，請側邊欄更新
        }
    } catch (error) {
        console.error("儲存失敗：", error);
        alert("儲存失敗，請檢查後端連線！");
    }
}

const handleImageUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
            editor.value.chain().focus().setImage({ src: e.target.result }).run()
        }
        reader.readAsDataURL(file)
    }
}
const triggerImageUpload = () => {
    document.getElementById('image-upload').click()
}

//Extension設定
const CustomSlashCommand = Extension.create({
  name: 'customSlashCommand',

  addProseMirrorPlugins() {
    return [
      Suggestion({
        editor: this.editor,
        char: '/',
        // 選單呼叫 props.command(item) 時會走到這裡；必須轉呼叫該項目的 command，否則預設為 null 不會改文件
        command: ({ editor, range, props: item }) => {
          item.command({ editor, range })
        },
        items: ({ query }) => {
          return [
            { title: '標題 1', command: ({ editor, range }) => editor.chain().focus().deleteRange(range).setNode('heading', { level: 1 }).run() },
            { title: '標題 2', command: ({ editor, range }) => editor.chain().focus().deleteRange(range).setNode('heading', { level: 2 }).run() },
            { title: '粗體文字', command: ({ editor, range }) => editor.chain().focus().deleteRange(range).setMark('bold').run() },
            { title: '插入圖片', command: ({ editor, range }) => {
                editor.chain().focus().deleteRange(range).run();
                document.getElementById('image-upload').click();
            }},  
            { title: '待辦清單', command: ({ editor, range }) => editor.chain().focus().deleteRange(range).toggleTaskList().run() },
          ].filter(item => item.title.toLowerCase().startsWith(query.toLowerCase())).slice(0, 10)
        },

        render: () => {
          let component
          let popup

          return {
            onStart: props => {
              if (!props.clientRect) {
                return
              }
              // 1. 初始化 VueRenderer
              component = new VueRenderer(SlashMenuList, {
                props: {
                  items: props.items,
                  command: props.command,
                  onSelect: () => {
                    popup?.hide()
                  }
                },
                editor: this.editor,
                on: {
                  select: () => {
                    popup?.hide()
                  }
                }
              })

              // 2. 初始化 Tippy（傳 document.body 才會得到單一 Instance；字串選擇器在 v6 會回傳陣列）
              popup = tippy(document.body, {
                getReferenceClientRect: props.clientRect,
                appendTo: () => document.body,
                content: component.element,
                showOnCreate: true,
                interactive: true,
                trigger: 'manual',
                placement: 'bottom-start',
              })
            },

            onUpdate(props) {
              component?.updateProps(props)
              if (!props.clientRect) {
                popup?.destroy()
                popup = null
                return
              }
              if (popup) {
                popup.setProps({
                  getReferenceClientRect: props.clientRect,
                })
              }
            },

            onKeyDown(props) {
              if (props.event.key === 'Escape') {
                popup?.hide()
                return true
              }
              // 呼叫 Vue 組件內暴露的 onKeyDown 方法
              return component.ref?.onKeyDown(props)
            },

            onExit() {
              popup?.destroy()
              component?.destroy()
            },
          }
        },
      }),
    ]
  },
})

const editor = useEditor({
    extensions:[
        CustomSlashCommand,
        StarterKit,
        Placeholder.configure({
            placeholder:"輸入 '/' 開啟指令選單..."
        }),
        Highlight,
        TaskList,
        TaskItem,
        Image.configure({
            allowBase64: true,
            HTMLAttributes: {
                class: 'editor-image'
            }
        })
    ],
    content: '',
})

watch(() => props.currentNote, (newNote) => {
    if (newNote) {
        title.value = newNote.title || '';
        // 加上 editor.value 的檢查，避免編輯器還沒準備好就塞資料
        if (editor.value) {
            editor.value.commands.setContent(newNote.body_content || ''); 
        }
    } else {
        title.value = '';
        if (editor.value) {
            editor.value.commands.setContent('');
        }
    }
}, { immediate: true })

</script>
<template>
 <div class="editor-workspace">
            <div class="sticky-header">
                <div class="title-container">
                    <input 
                    type="text" 
                    v-model="title"
                    placeholder="請輸入筆記標題..."
                    class="title-input">
                </div>
                <div class="toolbar">
                    <button @click="toggleBold()" class="toolbar-button"><b>B</b></button>
                    <button @click="toggleHeading()" class="toolbar-button">H1</button>
                    <button @click="toggleHighlight()" class="toolbar-button">螢光筆</button>
                    <button @click="toggleTaskList()" class="toolbar-button">待辦清單</button>
                    <button @click="toggleCodeBlock()" class="toolbar-button">程式碼</button>
                    
                    <button @click="triggerImageUpload" class="toolbar-button">插入圖片</button>
                    <button @click="saveContent()" class="save-btn">儲存筆記</button>
                </div>
            </div>

            <input 
                type="file" 
                id="image-upload" 
                ref="imageInput" 
                accept="image/*" 
                style="display: none;" 
                @change="handleImageUpload">

            <editor-content :editor="editor" class="editor-container" />
        </div>
    </template>
<style scoped>
.editor-workspace {
    flex: 1;
    overflow-y: auto;
    padding: 0 100px 60px 100px; 
    
    /* 增加以下三行 */
    box-sizing: border-box; /* 確保 padding 不會額外增加高度 */
    min-height: 0; /* 覆蓋 Flex 預設行為，避免被內容無限撐大 */
    height: 100vh; /* 明確綁定高度 */
}
.sticky-header {
            position: sticky;
            top: 0;
            background-color: #ffffff; 
            z-index: 100;
            padding: 20px 0 15px 0; 
            border-bottom: 1px solid #edece9; 
            margin-bottom: 30px;
        }
.title-container{
    max-width: 800px; 
    margin: 0 auto 10px auto;
}
.title-input{
    width: 100%; 
    border: none; 
    font-size: 24px; 
    font-weight: bold; 
    outline: none; 
    padding: 10px 0; 
    background-color: transparent
}
.toolbar {
            max-width: 800px;
            margin: 0 auto 30px auto;
            display: flex;
            gap: 10px;
            padding-bottom: 10px;
            border-bottom: 1px solid #f1f1f1;
            margin-bottom: 0;
        }
.toolbar-button {
    background: white;
    border: 1px solid #ddd;
    padding: 5px 12px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 13px;
    transition: background 0.2s;
}

.toolbar button:hover {
    background: #f1f1f1;
}

.save-btn {
    border-radius: 4px;
    background: #2383e2 !important;
    color: white !important;
    border: none !important;
}
/*placeholder顯示出來 */
:deep(.ProseMirror p.is-editor-empty:first-child::before){
    content: attr(data-placeholder);
    float: left;
    color: #adb5ad;
    pointer-events: none;
    height:0;
}
.editor-container {
    max-width: 800px;
    margin: 0 auto;
}
:deep(.ProseMirror) {
    min-height: 300px; 
    outline: none;   
    padding: 20px 0;
    font-size: 16px;
    line-height: 1.6;
}
/* 針對編輯器內的圖片設定最大顯示大小 */
:deep(.editor-image) {
    max-width: 100%;      /* 確保圖片寬度絕對不會超出編輯器的範圍 */
    max-height: 400px;    /* 設定圖片的最大高度 (你可以依需求改成 300px 或 500px) */
    object-fit: contain;  /* 確保圖片縮放時不會變形 */
    display: block;       /* 讓圖片變成區塊元素，方便排版 */
    border-radius: 8px;   /* (可選) 讓圖片有一點圓角，看起來更好看 */
    margin: 10px 0;       /* (可選) 讓圖片上下留一點空白 */
}
</style>