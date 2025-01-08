from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from accounts.forms import LoginForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Profile


# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password']
                                )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Muvaffaqiyatli login amalga oshirildi!')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas!')
            else:
                return HttpResponse('Login va parolda hatolik bor!')
    else:
        form = LoginForm()
        context = {
            'form': form
        }
    return render(request, 'registration/login.html', {'form': form})


# @login_required
# def dashboard_views(request):
#     user = request.user
#     profil_info = Profile.objects.get(user=user)
#     context = {
#         'user': user,
#         'profil_info': profil_info
#     }
#     return render(request, 'pages/user_profile.html', context)
