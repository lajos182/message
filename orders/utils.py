import json
from django.http import HttpResponse

def win_response(code=1, message='success', data=None, status=200):
    rep_dict = {
        'code': code,
        'message': message,
        'data': data
    }
    return HttpResponse(content=json.dumps(rep_dict, ensure_ascii=False), content_type="application/json;charset=UTF-8",status=status)

def lose_response(code=0, message='failed', data=None, status=400):
    rep_dict = {
        'code': code,
        'message': message,
        'data': data
    }
    return HttpResponse(content=json.dumps(rep_dict, ensure_ascii=False), content_type="application/json;charset=UTF-8",status=status)