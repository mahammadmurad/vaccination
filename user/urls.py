from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.login, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    path('profile-view/', views.profile_view, name='profile_view'),
    path('profile-update/', views.profile_update, name='profile_update'),
]