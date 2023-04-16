from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models.functions import Lower
from .forms import VideoForm, SearchForm
from .models import Video

def home(request):
    app_name = 'Music Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

# this is the new add function to add a video
def add(request):
    if request.method == 'POST': # if POST (creating new video)
        new_video_form = VideoForm(request.POST) # VideoForm class that was created from the data that was sent to the server's part of POST request

        if new_video_form.is_valid(): # is_valid() is a method built in already
            try:
              new_video_form.save() # if valid, save to database
              return redirect('video_list')
              # messages.info(request, 'New video saved!')

            except ValidationError:
                messages.warning(request, 'Invalid Youtube URL')
            except IntegrityError:
                messages.warning(request, 'You already added that video')

        messages.warning(request, 'Please check the data entered.')
        return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})
    
    # if not POST request or above code was successfully saved,
    # this part of the code will execute,
    # empty and ready to go to submit new video
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})

# this will get all the videos from Video Model
def video_list(request):
    search_form = SearchForm(request.GET) # build form from data user has sent to app

    if search_form.is_valid():
        search_term = search_form.cleaned_data['search_term'] # example: 'logic' -- search_term - same as the one in forms.py. 
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) # name__icontains is a django query

    else: # form is not filled in or this is the first time the user sees the page
        search_form = SearchForm()
        videos = Video.objects.all().order_by(Lower('name'))
    
    return render(request, 'video_collection/video_list.html', {'videos': videos, 'search_form': search_form})


def video_detail(request, video_pk):
    details = get_object_or_404(Video, pk=video_pk)
    return render(request, 'video_collection/video_detail.html', {'details': details})