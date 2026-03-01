# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import UserRegisterForm, UserLoginForm

# Đăng ký
@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tài khoản đã được tạo! Bạn có thể đăng nhập ngay.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Đăng nhập
@ensure_csrf_cookie
def login_user(request):
    next_url = request.GET.get('next') or request.POST.get('next')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)   # luôn truyền request
        if form.is_valid():
            user = form.get_user()                         # không cần authenticate lại
            login(request, user)

            # (tùy chọn) "Ghi nhớ đăng nhập"
            if request.POST.get("remember") != "on":
                request.session.set_expiry(0)  # hết phiên trình duyệt

            messages.success(request, f'Chào mừng {user.get_username()} đã đăng nhập!')
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
            ):
                return redirect(next_url)
            return redirect('map_view')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    else:
        form = UserLoginForm(request)  # truyền request ở GET luôn

    ctx = {'form': form, 'next': next_url}
    return render(request, 'users/login.html', ctx)

# Đăng xuất (POST-only)
@require_POST
def logout_user(request):
    logout(request)
    messages.info(request, 'Bạn đã đăng xuất.')
    return redirect('login')
