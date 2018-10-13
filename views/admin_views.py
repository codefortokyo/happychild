from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from infrastructure.models import Nursery, Ward
from services.forms.admins import NurseryForm


@login_required
def nursery_list(request: HttpRequest, ward_id: int) -> render:
    return render(request, 'admin/nursery_list.html', context={
        'nurseries': Nursery.objects.filter(ward_id=ward_id).order_by('-updated_at'),
        'ward': Ward.objects.filter(id=ward_id).first()
    })


@login_required
def nursery(request: HttpRequest, ward_id: int, nursery_id: int) -> render or redirect:
    if request.method == 'GET':
        return render(request, 'admin/nursery.html', context={
            'ward': Ward.objects.filter(id=ward_id).first(),
            'nursery_id': nursery_id,
            'form': NurseryForm(instance=Nursery.objects.get(pk=nursery_id))
        })
    form = NurseryForm(request.POST, instance=Nursery.objects.get(pk=nursery_id))
    if form.is_valid():
        form.save()
        return redirect('/admin/wards/{}/nurseries/'.format(ward_id))
    return render(request, 'admin/nursery.html', context={
        'ward': Ward.objects.filter(id=ward_id).first(),
        'nursery_id': nursery_id,
        'form': form
    })

