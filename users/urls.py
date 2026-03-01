from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    # Đăng xuất bằng POST, xong chuyển về trang login
    path('logout/', views.logout_user, name='logout'),
]
