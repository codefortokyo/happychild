from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from infrastructure.consts import DayOfWeek
from infrastructure.models import Nursery, UserNurseryMapping, NurseryDefaultTourSetting, NurseryTours
from services.forms.admins import NurseryForm, NurseryFreeNumForm, NurseryDefaultTourForm


@login_required
def nursery_list_profile(request: HttpRequest, user_id: int) -> render or redirect:
    return render(request, 'profile/organizer/nursery_list.html', context={
        'nurseries': sorted([n.nursery for n in
                             UserNurseryMapping.objects.select_related('nursery').filter(user_id=user_id)],
                            key=lambda x: x.updated_at, reverse=True)
    })


@login_required
def nursery_basic_profile(request: HttpRequest, user_id: int, nursery_id: int) -> render or redirect:
    if request.method == 'GET':
        return render(request, 'profile/organizer/nursery.html', context={
            'nursery_id': nursery_id,
            'form': NurseryForm(instance=Nursery.objects.get(pk=nursery_id)),
        })
    form = NurseryForm(request.POST, instance=Nursery.objects.get(pk=nursery_id))
    if form.is_valid():
        form.save()
        return redirect('/user/{}/nurseries/{}/basic'.format(user_id, nursery_id))
    return render(request, 'profile/organizer/nursery.html', context={
        'nursery_id': nursery_id,
        'form': form,
    })


@login_required
def nursery_free_num_profile(request: HttpRequest, user_id: int, nursery_id: int) -> render or redirect:
    if request.method == 'GET':
        return render(request, 'profile/organizer/nursery_free_num.html', context={
            'nursery_id': nursery_id,
            'form': NurseryFreeNumForm(),
        })
    form = NurseryFreeNumForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/{}/nurseries/{}/free'.format(user_id, nursery_id))
    return render(request, 'profile/organizer/nursery.html', context={
        'nursery_id': nursery_id,
        'form': form,
    })


@login_required
def nursery_tour_profile(request: HttpRequest, user_id: int, nursery_id: int) -> render or redirect:
    if request.method == 'GET':
        return render(request, 'profile/organizer/nursery_tour.html', context={
            'nursery_id': nursery_id,
            'form': NurseryDefaultTourForm(instance=NurseryDefaultTourSetting.get_settings(nursery_id)),
        })
    form = NurseryDefaultTourForm(request.POST, instance=NurseryDefaultTourSetting.get_settings(nursery_id))
    if form.is_valid():
        NurseryDefaultTourSetting.objects.update_or_create(
            nursery=Nursery.get_nursery(nursery_id),
            defaults={
                'start_time': form.cleaned_data['start_time'],
                'end_time': form.cleaned_data['end_time'],
                'capacity': form.cleaned_data['capacity'],
                'description': form.cleaned_data['description'],
                'note': form.cleaned_data['note'],
            })
        NurseryTours.create_tour_schedules_in_a_month(nursery_id, DayOfWeek.get_default_held_days(), True)
        return redirect('/user/{}/nurseries/{}/tour'.format(user_id, nursery_id))
    return render(request, 'profile/organizer/nursery.html', context={
        'nursery_id': nursery_id,
        'form': form,
    })
