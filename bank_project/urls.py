# bank_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Các App chức năng
    path('users/', include('users.urls')),
    path('map/', include('map.urls')),
    
    # URL mặc định của Django Auth (login/logout/password_reset)
    path('accounts/', include('django.contrib.auth.urls')),  
    
    # ========================================================
    # 1. SỬA QUAN TRỌNG: Phải đặt tên là 'test-dashboard/' 
    # để khớp với code Javascript fetch('/test-dashboard/run/...')
    # ========================================================
    path('test-dashboard/', include('test_dashboard.urls')),

    # 2. LOGIN: Nếu bạn đã có file template ở 'users/login.html' 
    # thì nên chỉ định rõ template_name để tránh lỗi TemplateDoesNotExist
   # SỬA DÒNG NÀY: Đổi 'users/login.html' thành 'registration/login.html'
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    # Logout: Logout xong quay về trang chủ ('/')
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Redirect trang chủ: Nếu chưa biết đi đâu thì vào login
    path('', lambda request: redirect('login')),
]