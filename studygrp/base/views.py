from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import RoomForm, UserForm, CustomUserCreationForm
from .models import Room, Topic, Message, User

# Create your views here.

def loginPage(request): # There is an in-built login method so do not name this login
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User not found.')
            return redirect('login')
        
        # returns user as None if the user password does not match
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password incorrect.')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = CustomUserCreationForm()
    context = {'page': page, 'form': form}
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Saves the data into user Object but not into the database yet
            user.username = user.username.lower() # makes sure consistency for user names into lower case
            user.save() # Saves the user to the database
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')

    return render(request, 'base/login_register.html', context)

def home(request):
    # request is the http object
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)) # runs the filter if topic_name contains a non empty string (ignoring caps, else just gives all the Rooms since all rooms contains '')
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    rooms_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'rooms_messages': rooms_messages} 
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() # Gives us the set of Message Model instances referencing this room, ordered by created (descending).
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room= room,
            body=request.POST.get('body')
            ) # Creates a model instance of Message
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    rooms_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'rooms_messages': rooms_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login') # Decorator to redirect non-logged in user to login page
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        
        # Returns the topic object and a boolean value. The boolean is true when a new Topic is created. 
        # If not created (available in database) then created will be false.
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(host=request.user, topic=topic, name=request.POST.get('name'), description=request.POST.get('description'))
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     form.save()
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # pre-fills the RoomForm with the room attribute values
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Only update rooms that are your own!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('Only delete rooms that are your own!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    room_message = Message.objects.get(id=pk)
    if request.user != room_message.user:
        return HttpResponse('Only delete messages that are your own!')
    if request.method == 'POST':
        room_message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room_message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
            
    context = {'form': form}
    return render(request, 'base/update-user.html', context=context)
    pass

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

def activitiesPage(request):
    rooms_messages = Message.objects.all()[0:5]
    context = {'rooms_messages': rooms_messages}
    return render(request, 'base/activity.html', context)