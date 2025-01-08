from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
urlpatterns = [
    # path('login/', user_login, name='login')
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post', 'options']), name='logout'),
    # path('profile/', dashboard_views, name='profile_page'),
]
