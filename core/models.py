import uuid
from django.db import models

class Note(models.Model):
    # 選項 1: 使用 Django 預設的自動遞增 ID (不寫這行也可以，Django 會自動加)
    # 適合簡單的專案
    # id = models.BigAutoField(primary_key=True)
    
    # 選項 2: 使用 UUID 作為主鍵 (推薦)
    # 更符合現代編輯器 (如 Notion) 的架構，前端產生的 ID 不易被猜測
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    title = models.CharField(max_length=200, default="未命名筆記")
    
    # 儲存 Tiptap 傳來的整包 JSON 內容
    content_json = models.JSONField(null=True, blank=True)
    
    # 建立時間：只有在新增 (Create) 時會自動記錄
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 修改時間：每次呼叫 .save() 執行 Update 時，會自動更新此時間
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title