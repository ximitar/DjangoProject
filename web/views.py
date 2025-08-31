from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page


from web.forms import RegistrationForm, AuthForm, RoomForm, RoomFilterForm
from .models import Room, RoomParticipant

# Create your views here.

User = get_user_model()


def main_view(request):
    year = datetime.now().year
    return render(request, 'web/main.html', {
        'year': year,
    })


def registartion_view(request):
    form = RegistrationForm()
    is_succses = False
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(form.cleaned_data)
            is_succses = True
    return render(request, "web/registration.html",
                  {'form': form, 'is_succses': is_succses,
                   })


def auth_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, "Пользователь не найден")
            else:
                login(request, user)
                return redirect('main')

    return render(request, 'web/auth.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('main')


@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.creator = request.user
            room.save()
            form.save_m2m()

            room_participant, created = RoomParticipant.objects.get_or_create(
                user=request.user, room=room)
            if created:
                room_participant.save()
            return redirect('room_list')
    else:
        form = RoomForm()

    return render(request, 'create_room.html', {'form': form})


@cache_page(10)
@login_required
def room_list(request):
    rooms = Room.objects.all()
    page_number = request.GET.get('page', 1)
    room_filter_form = RoomFilterForm(request.GET)
    room_filter_form.is_valid()
    filter = room_filter_form.cleaned_data

    if filter['search']:
        rooms = Room.objects.filter(room_name__icontains=filter['search'])

    paginator = Paginator(rooms, per_page=10)

    return render(request, 'room_list.html', {'rooms': paginator.get_page(page_number), 'room_filter_form': room_filter_form})


def is_room_participant(user, room_id):
    return RoomParticipant.objects.filter(user=user, room_id=room_id).exists()


@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def room_detail(request, room_id):

    if not is_room_participant(request.user, room_id):
        return redirect('/room_list/')

    room = get_object_or_404(Room, id=room_id)
    participants = RoomParticipant.objects.filter(room=room)
    participants = room.participants.all()
    return render(request, 'room_detail.html', {'room': room, 'participants': participants})


@login_required
def join_room_from_list(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id', None)
        entered_password = request.POST.get('password', '')
        if room_id:
            room = get_object_or_404(Room, id=room_id)
            if entered_password == room.password:
                room_participant, created = RoomParticipant.objects.get_or_create(
                    user=request.user, room=room)
                if created:
                    room_participant.save()
                return redirect('room_detail', room_id=room.id)
            else:
                messages.error(
                    request, 'Incorrect password. Please try again.')

    return redirect('room_list')
