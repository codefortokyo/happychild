from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from infrastructure.models import Nursery, NurseryFreeNum, Ward
from infrastructure.consts import NURSERY_INFO, NURSERY_FREE_NUM, NURSERY_SCORE
from services.forms.admins import NurseryForm, NurseryFreeNumForm
from services.transformers import transform_free_num_form_to_free_num


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
            'form': NurseryForm(instance=Nursery.objects.get(pk=nursery_id)),
            'form_free_num': NurseryFreeNumForm()
        })

    form_type = request.POST.get('form_type')

    if form_type == NURSERY_INFO:
        form = NurseryForm(request.POST, instance=Nursery.objects.get(pk=nursery_id))
        if form.is_valid():
            form.save()
            return redirect('/admin/wards/{}/nurseries/'.format(ward_id))

    elif form_type == NURSERY_FREE_NUM:
        form = NurseryFreeNumForm(request.POST)
        if form.is_valid():
            entities = transform_free_num_form_to_free_num(form, nursery_id)
            NurseryFreeNum.bulk_insert(entities)
            return redirect('/admin/wards/{}/nurseries/'.format(ward_id))

    return render(request, 'admin/nursery.html', context={
        'ward': Ward.objects.filter(id=ward_id).first(),
        'nursery_id': nursery_id,
        'form': NurseryForm(request.POST, instance=Nursery.objects.get(pk=nursery_id)),
        'form_free_num': NurseryForm(request.POST),
    })
