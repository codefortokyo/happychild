import json
from typing import Union

from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from infrastructure.models import CustomUser, Nursery, NurseryBookmark


@csrf_exempt
def register_bookmark(request: HttpRequest) -> HttpResponse:
    user_id = request.POST.get('user_id')
    nursery_id = request.POST.get('nursery_id')
    response_data = {}

    if not user_id or not nursery_id:
        response_data['message'] = 'パラメータが不足しています'
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    if not _validate_register_bookmark(user_id, nursery_id):
        response_data['message'] = 'パラメータ値が不正です'
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=400)

    NurseryBookmark.register_bookmark(user_id, nursery_id)
    response_data['message'] = 'success'
    return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)


def _validate_register_bookmark(user_id: int, nursery_id: int) -> Union[bool, str]:
    return True if _nursery_is_exist(nursery_id) and _user_is_exist(user_id) else False


def _nursery_is_exist(nursery_id: int) -> bool:
    return Nursery.objects.filter(id=nursery_id).exists()


def _user_is_exist(user_id: int) -> bool:
    return CustomUser.objects.filter(id=user_id).exists()
