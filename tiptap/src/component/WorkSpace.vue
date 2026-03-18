<script setup>
import { ref } from 'vue'
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

const saveContent = () => {
    console.log("儲存內容：", editor.value.getHTML())
    alert("內容已儲存！(請對接後端 API)")
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
//Extension設定
const CustomSlashCommand = Extension.create({
  name: 'customSlashCommand',

  addProseMirrorPlugins() {
    return [
      Suggestion({
        editor: this.editor,
        char: '/',
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
                  command: props.command
                },
                editor: this.editor,
              })

              // 2. 初始化 Tippy (用來做浮動定位)
              popup = tippy('body', {
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
const title = ref('')

const editor = useEditor({
    extensions:[
        CustomSlashCommand,
        StarterKit,
        Placeholder.configure({
            placeholder:"輸入 '/' 開啟指令選單..."
        })
    ],
    content: '',
})
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
                    
                    <button @click="document.getElementById('image-upload').click()" class="toolbar-button">插入圖片</button>
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
            padding: 0 100px 60px 100px; /* 改為上0, 右100, 下60, 左100 */
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
</style>