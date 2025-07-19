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
]