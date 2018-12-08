import json
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from infrastructure.models import CustomUser, NurseryBookmark, NurseryTour, NurseryReservation
from services.details import get_nursery
from services.forms.reservations import NurseryReservationForm


def nursery_detail(request: HttpRequest, nursery_id: int) -> render:
    nursery = get_nursery(nursery_id)
    nursery_tours = NurseryTour.get_nursery_tours(nursery_id)
    for nursery_tour in nursery_tours:
        if not request.user:
            nursery_tour.is_reserved = False
        nursery_tour.is_reserved = NurseryReservation.objects.filter(nursery_tour_id=nursery_tour.id,
                                                                     user_id=request.user.id).exists()
    return render(request, 'nursery/detail.html', context={
        'nursery': nursery,
        'nursery_tours': nursery_tours,
        'is_bookmarked': NurseryBookmark.is_bookmarked(request.user.id, nursery_id) if request.user else False,
        'nursery_json': json.dumps({'data': [json.loads(nursery.to_json())]})
    })


@login_required
def nursery_reservation(request: HttpRequest, nursery_id: int, nursery_tour_id: int,
                        reservation_id: Optional[int] = None) -> render:
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'GET':
        if reservation_id:
            reservation = NurseryReservation.objects.select_related('user').get(pk=reservation_id)
            form = NurseryReservationForm(initial={
                'name': reservation.user.name,
                'email': reservation.user.email,
                'address': reservation.user.address,
                'phone_number': reservation.user.phone_number,
                'note': reservation.note,
            }, instance=reservation)
        else:
            form = NurseryReservationForm(initial={
                'name': user.name,
                'email': user.email,
                'address': user.address,
                'phone_number': user.phone_number,
            })
        return render(request, 'nursery/reservation.html', context={
            'nursery_tour': NurseryTour.objects.select_related('nursery').get(pk=nursery_tour_id),
            'reservation_id': reservation_id or None,
            'nursery_id': nursery_id,
            'form': form,
        })
    form = NurseryReservationForm(request.POST)
    if form.is_valid():
        NurseryReservation.objects.update_or_create(
            nursery_tour=NurseryTour.objects.get(pk=nursery_tour_id),
            user=user,
            defaults={
                'note': form.cleaned_data.get('note', '')
            }
        )
        return redirect('/nursery/{}'.format(nursery_id))
    return render(request, 'nursery/reservation.html', context={
        'nursery_tour': NurseryTour.objects.select_related('nursery').get(pk=nursery_tour_id),
        'nursery_id': nursery_id,
        'reservation_id': reservation_id or None,
        'form': form,
    })
