from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Room, Topic
from crud_app.form_data import FormCreation
from django.db.models import Q


# room_data = [
#     {"id": 1, "name": "QueeryLoad", "strength": "Massive"},
#     {"id": 2, "name": "ActionMonster", "strength": "Less"},
#     {"id": 3, "name": "ListyToal", "strength": "Dominant"},
#     {"id": 4, "name": "Bealine", "strength": "Concord"},
# ]


# Create your views here.
def main(request):
    return render(request, 'main.html')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ""
    roomers = Room.objects.all().filter(
        Q(topic__name__icontains=q) or
        Q(name__icontains=q) or
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = roomers.count()
    return render(request, 'home.html',
                  {
                            "roomers": roomers,
                            'topics': topics,
                            'room_count': room_count,

                   })


def room(request, pk):
    room_case = Room.objects.get(id=pk)
    room_messages = room_case.message_set.all()
    context = {'room_case': room_case,'room_messages': room_messages}
    return render(request, 'crud_app/room.html', context)


@login_required(login_url='/login')
def createRoom(request):
    form = FormCreation()
    if request.method == 'POST':
        form_request = FormCreation(request.POST)
        if form_request.is_valid():
            form_request.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'crud_app/room_form.html', context)


@login_required(login_url='/login')
def updateRoom(request, pk):
    get_room = Room.objects.get(id=pk)
    form = FormCreation(instance=get_room)
    if request.method == 'POST':
        form = FormCreation(request.POST, instance=get_room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'crud_app/room_form.html', context)


@login_required(login_url='/login')
def deleteRoom(request, pk):
    get_room = Room.objects.get(id=pk)
    context = {'obj': get_room}
    if request.method == 'POST':
        get_room.delete()
        return redirect("home")
    return render(request, 'crud_app/deleteRoom.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')


def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    context = {'page': page}
    return render(request, 'crud_app/login_register.html', context)


def registerPage(request):
    # page = 'register'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('logger_in')
            # return redirect('login')
        else:
            messages.error(request, "Error occurred during registration")

    return render(request, 'crud_app/login_register.html', {'form': form})
