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
            # 將 Tiptap 傳來的 body_content 存入 JSONField
            new_note = Note.objects.create(
                content_json=data.get('body_content')
            )
            return JsonResponse({'status': 'success', 'id': new_note.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'failed'}, status=405)

def get_latest_note(request):
    try:
        # 抓取最後一筆筆記
        note = Note.objects.latest('created_at') 
        return JsonResponse({
            'status': 'success',
            'body_content': note.content_json
        })
    except Note.DoesNotExist:
        return JsonResponse({'status': 'empty', 'message': '尚無筆記'}, status=200)

def note_list(request):
    # 取得所有筆記，按時間倒序排列
    notes = Note.objects.all().order_order_by('-created_at')
    return render(request, 'notes.html', {'notes': notes})

def get_all_notes(request):
    # 取得資料庫中所有的筆記，按時間倒序排列
    notes = Note.objects.all().order_by('-created_at')
    notes_data = []
    
    for note in notes:
        notes_data.append({
            'id': note.id,
            'body_content': note.content_json,
            'created_at': note.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
        
    return JsonResponse({
        'status': 'success',
        'notes': notes_data
    })