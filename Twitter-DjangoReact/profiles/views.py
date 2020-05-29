from django.http import Http404
from django.shortcuts import render, redirect

from .models import Profile
from .forms import ProfileForm

"""
Function based views for rendering and handling the detail/update view. 
"""
def profile_detail_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        raise Http404

    profile_obj = qs.first()
    is_following = False 
    if request.user.is_authenticated:
        is_following = request.user in profile_obj.followers.all()
    context = {
        'username': username,
        'profile': profile_obj, 
        'is_following': is_following,
    }
    return render(request, "profiles/detail.html", context=context)

def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/login?next=/profile/update')
    
    user = request.user 
    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    my_profile = user.profile 
    form = ProfileForm(request.POST or None, instance=my_profile, initial=user_data)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        firstname = form.cleaned_data.get('first_name')
        lastname = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        user.first_name = firstname
        user.last_name = lastname
        user.email = email 
        user.save()
        profile_obj.save()
    context = {
        'form': form, 
        'btn_laebl': 'Save',
        'title': 'Update Profile'
    }
    return render(request, 'profiles/form.html', context=context)
