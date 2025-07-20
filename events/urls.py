from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('approval/', views.approval_view, name='approval'),
    path('approve_all/', views.approve_all, name='approve_all'),
    path('profile/organiser/', views.profile_view_organiser, name='profile_org'),
    path('profile/participant/', views.profile_view_participant, name='profile_participant'),
    path('create_event/', views.create_event_view, name='create_event'),
    path('upcoming_events/', views.upcoming_events_view, name='upcoming_events'),
    path('live_events/', views.live_events_view, name='live_events'),
    path('event/<int:event_id>/', views.register_event_view, name='register_events'),
]