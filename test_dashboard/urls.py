from django.urls import path
from . import views

urlpatterns = [
    # 1. Trang hiển thị Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # 2. API chạy test (Nút Xanh và Vàng)
    path('run/', views.run_tests, name='run_tests'),
    
    # 3. API đóng trình duyệt (Nút Đỏ) -> BẠN ĐANG THIẾU CÁI NÀY
    path('close-browsers/', views.close_browsers, name='close_browsers'),

    # 4. Link nạp data ban đầu
    path('init/', views.init_data, name='init_data'), 
]