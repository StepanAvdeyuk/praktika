from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home_page, name='home'),
    path('', views.Scope.as_view(), name='home'),
    path('oscilloscope/', views.Scope.as_view(), name='scope'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('pass_reset', views.reset_page, name='password_reset'),
]
