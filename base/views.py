from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, City, Message, User
from .forms import RoomForm, UserForm , MyUserCreationForm
from datetime import datetime
from django.contrib.auth.forms import PasswordResetForm


# Create your views here.


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'You are successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.error(request, 'You have been logged out')
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')


    return render(request, 'base/login_register.html',  {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(city__name__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    

    topics = Topic.objects.all()[0:5]
    cities = City.objects.all()[0:5]
    room_count = rooms.count()
    # room_messages = Message.objects.filter(
    #     Q(room__city__name__icontains=q))[0:3]
    room_messages = Message.objects.filter(
    Q(room__city__name__icontains=q) | Q(room__topic__name__icontains=q)
    )[:3]
    paginated_by = 2
    context = {'rooms': rooms, 'cities': cities,
               'room_count': room_count, 'room_messages': room_messages, 'topics':topics}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def room(request, pk):
    # room = Room.objects.get(id=pk)
    room = get_object_or_404(Room, id=pk)
    room_messages = room.message_set.order_by('created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}        
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def userProfile(request, pk):
    # user = User.objects.get(id=pk)
    user = get_object_or_404(User, id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()[0:5]
    cities = City.objects.all()[0:5]
    
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics,'cities': cities}

    if request.user == user:
        context['delete_user'] = True

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    cities = City.objects.all()

    if request.method == 'POST':
        city_name = request.POST.get('city')
        city, created = City.objects.get_or_create(name=city_name)

        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        distance = request.POST.get('distance')
        if not distance:
            distance = 0  # Set distance to 0 if it's empty

        duration_minutes = request.POST.get('duration_minutes')
        if not duration_minutes:
            duration_minutes = 0  # Set duration_minutes to 0 if it's empty

        # location = request.POST.get('location')
        # if not location:
        #     location = ""  

        # days = request.POST.get('days')
        # if not days:
        #     days = 0  

        start_datetime_str = request.POST.get('start_datetime')
        start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')

        Room.objects.create(
            host=request.user,
            topic=topic,
            city=city,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            duration_minutes=duration_minutes,
            distance=distance,
            start_datetime=start_datetime,
            # location=location,
            # days=days
        )
        return redirect('home')

    context = {'form': form, 'topics': topics, 'cities': cities}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    cities = City.objects.all()
    
    # start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        city_name = request.POST.get('city')
        city, created = City.objects.get_or_create(name=city_name)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic

        room.name = request.POST.get('name')
        
        room.city = city
        room.description = request.POST.get('description')
        room.duration_minutes = request.POST.get('duration_minutes')
        room.distance = request.POST.get('distance')
        room.start_datetime = request.POST.get('start_datetime')

        # room.location = request.POST.get('location')
        # room.days = request.POST.get('days')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'cities': cities, 'room': room} 
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def deleteUser(request):
    if request.method == 'POST':
        user = request.user
        # Perform any additional cleanup or related deletion tasks here if needed
        user.delete()
        logout(request)
        messages.success(request, 'Your profile has been deleted')
        return redirect('home')

    return render(request, 'base/delete_user.html', {'obj': request.user})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})




def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})


def cityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    cities = City.objects.filter(name__icontains=q)
    return render(request, 'base/cities.html', {'cities': cities})
