from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('play/',views.play,name='play'),
    path('sneak-peak/', views.sneakPeak, name='sneakPeak'),
    path('hint/', views.hint, name='hint'),
    path('re-roll/', views.reRoll, name='reRoll'),
    path('get-head/', views.getHead, name='getHead'),
]