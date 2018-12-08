import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from infrastructure.models import CustomUser, NurseryBookmark, NurseryTours, NurseryReservation
from services.details import get_nursery
from services.forms.reservations import NurseryReservationForm


def nursery_detail(request: HttpRequest, nursery_id: int) -> render:
    nursery = get_nursery(nursery_id)
    nursery_tours = NurseryTours.get_nursery_tours(nursery_id)
    return render(request, 'nursery/detail.html', context={
        'nursery': nursery,
        'nursery_tours': nursery_tours,
        'is_bookmarked': NurseryBookmark.is_bookmarked(request.user.id, nursery_id) if request.user else False,
        'nursery_json': json.dumps({'data': [json.loads(nursery.to_json())]})
    })


@login_required
def nursery_reservation(request: HttpRequest, nursery_id: int, nursery_tour_id: int) -> render:
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'GET':
        form = NurseryReservationForm(initial={
            'name': user.name,
            'email': user.email,
            'address': user.address,
            'phone_number': user.phone_number,
        })
        return render(request, 'nursery/reservation.html', context={
            'nursery_tour': NurseryTours.objects.get(pk=nursery_tour_id),
            'nursery_id': nursery_id,
            'form': form,
        })
    form = NurseryReservationForm(request.POST)
    if form.is_valid():
        reservation = NurseryReservation(
            nursery_tour=NurseryTours.objects.get(pk=nursery_tour_id),
            user=user,
            note=form.cleaned_data.get('note', '')
        )
        reservation.save()
        return redirect('/nursery/{}'.format(nursery_id))
    return render(request, 'nursery/reservation.html', context={
        'nursery_tour': NurseryTours.objects.get(pk=nursery_tour_id),
        'nursery_id': nursery_id,
        'form': form,
    })
