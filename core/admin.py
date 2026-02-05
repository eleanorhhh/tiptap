from django.contrib import admin
from .models import Note  # 這裡要跟 models.py 裡定義的名字一模一樣

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')