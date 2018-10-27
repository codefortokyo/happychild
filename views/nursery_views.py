import json

from django.shortcuts import render
from django.http import HttpRequest

from services.details import get_nursery


def nursery_detail(request: HttpRequest, nursery_id: int) -> render:
    nursery = get_nursery(nursery_id)
    return render(request, 'nursery/detail.html', context={
        'nursery': nursery,
        'nursery_json': json.dumps({'data': [json.loads(nursery.to_json())]})
    })
