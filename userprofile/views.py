from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt\



@login_required
@csrf_exempt
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user_details = form.save(commit=False)
            user_details.avatar = request.FILES['avatar']
            user_details.save()
            return redirect('/accounts/profile')
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)

    return render(request, 'userprofile/profile.html', {'form': form})
