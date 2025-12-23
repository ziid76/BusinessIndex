from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('user-management/', views.user_management, name='user_management'),
    path('update-user-permissions/', views.update_user_permissions, name='update_user_permissions'),
    path('daily-performance/<str:group_code>/', views.daily_performance, name='daily_performance'),
    path('save-performance/', views.save_performance, name='save_performance'),
]
