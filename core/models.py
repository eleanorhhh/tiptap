from django.db import models

# Create your models here.
class Note(models.Model):
    # 這裡存 Tiptap 傳過來的 JSON 內容
    content_json = models.JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)