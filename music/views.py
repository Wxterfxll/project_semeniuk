from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import PlaylistForm, RegistrationForm
from django.views.generic import TemplateView
from .models import Song, Playlist

class HomeView(TemplateView):
    template_name = 'music/home.html'

class LoginView(TemplateView):
    template_name = 'music/login.html'

class RegisterView(TemplateView):
    template_name = 'music/register.html'

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/') 
            return HttpResponseRedirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = RegistrationForm()
    return render(request, 'authentication/registration.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/') 
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def home(request):
    return render(request, 'music/home.html')

def song_list(request):
    songs = Song.objects.all()
    
    genres = songs.values_list('genre', flat=True).distinct()

    selected_genre = request.GET.get('genre')

    if selected_genre:
        songs = songs.filter(genre=selected_genre)

    return render(request, 'music/song_list.html', {'songs': songs, 'genres': genres})

def song_detail(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    user_playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'music/song_detail.html', {'song': song, 'playlists': user_playlists})

@login_required
def my_playlists(request):
    playlists_exist = Playlist.objects.filter(user=request.user).exists()
    my_playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'music/my_playlists.html', {'my_playlists': my_playlists, 'playlists_exist': playlists_exist})

@login_required
def create_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            playlist.save()
            return redirect('playlist_detail', playlist_id=playlist.id)
    else:
        form = PlaylistForm()
    return render(request, 'music/create_playlist.html', {'form': form})

@login_required 
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)\
        
    if request.user == playlist.user:
        if request.method == 'POST':
            playlist.delete()
            return redirect('my_playlists')
        return render(request, 'music/playlist_detail.html', {'playlist': playlist})
    else:
        return render(request, 'music/home.html')
    
 
@login_required
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    
    if request.user == playlist.user:
        return render(request, 'music/playlist_detail.html', {'playlist': playlist})
    else:
        return render(request, 'music/home.html')

@login_required
def add_to_playlist(request, song_id):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        song = get_object_or_404(Song, pk=song_id)
        playlist.songs.add(song)  
        return redirect('song_detail', song_id=song_id) 
    else:
        return redirect('song_list')  
    
@login_required
def remove_from_playlist(request, playlist_id, song_id):
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, pk=playlist_id)
        song = get_object_or_404(Song, pk=song_id)
        playlist.songs.remove(song)  
    return redirect('playlist_detail', playlist_id=playlist_id)  