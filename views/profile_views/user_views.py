from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect

from infrastructure.models import CustomUser as User
from infrastructure.models import NurseryBookmark
from services.forms.accounts import ProfileForm


@login_required
def user_profile(request: HttpRequest, user_id: int) -> render or redirect:
    if request.method == 'GET':
        return render(request, 'profile/user/user_settings.html', context={
            'user': User.get_user(user_id),
            'form': ProfileForm(instance=User.get_user(user_id))
        })
    form = ProfileForm(request.POST, instance=User.get_user(user_id))
    if form.is_valid():
        form.save()
        return redirect('user/{}'.format(user_id))
    return render(request, 'profile/user/user_settings.html', context={
        'user': User.get_user(user_id),
        'form': form
    })


@login_required
def bookmarked_nurseries(request: HttpRequest, user_id: int) -> render:
    return render(request, 'profile/user/bookmarked_nursery.html', context={
        'nurseries': NurseryBookmark.get_bookmarked(user_id=user_id)
    })
