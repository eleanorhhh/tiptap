import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Note
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["DELETE"])
@csrf_exempt
def delete_note(request, note_id):
    if request.method == 'DELETE':
        try:
            Note.objects.get(id=note_id).delete()
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'error'}, status=404)

@csrf_exempt   
def save_note(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note_id = data.get('id')
            title = data.get('title', '未命名筆記')
            content_json = data.get('body_content')

            if note_id:
                # 執行 Update (更新現有筆記)
                note = Note.objects.get(id=note_id)
                note.title = title
                note.content_json = content_json
                note.save()
            else:
                # 執行 Create (創建全新筆記)
                note = Note.objects.create(
                    title=title,
                    content_json=content_json
                )
            
            
            return JsonResponse({'status': 'success', 'id': str(note.id)})
        
        except Note.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '找不到指定的筆記進行更新'}, status=404)
        except Exception as e:
            print("❌ 儲存筆記發生錯誤:", str(e))
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def get_all_notes(request):
    notes = Note.objects.all().order_by('-created_at')
    notes_data = []
    for note in notes:
        notes_data.append({
            'id': str(note.id),
            'title': note.title, # 傳送標題
            'body_content': note.content_json,
            'created_at': note.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return JsonResponse({'status': 'success', 'notes': notes_data})

def note_list(request):
    # 取得所有筆記，按時間倒序排列
    notes = Note.objects.all().order_order_by('-created_at')
    return render(request, 'notes.html', {'notes': notes})



def get_note_by_id(request):
    note_id = request.GET.get('id') # 抓取 URL 中的 ?id=
    try:
        note = Note.objects.get(id=note_id)
        return JsonResponse({
            'status': 'success',
            'title': note.title,
            'body_content': note.content_json
        })
    except Note.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '找不到該筆記'}, status=404)