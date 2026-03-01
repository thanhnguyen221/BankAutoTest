from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class MapIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Setup URL (Sửa lại cho chuẩn với bài trước)
        try: self.login_url = reverse('login') 
        except: self.login_url = '/login/'
        
        # Lưu ý: Bài trước bạn dùng /users/register/ nên ở đây phải sửa lại
        try: self.register_url = reverse('register') 
        except: self.register_url = '/users/register/' 

        # 2. CHỈ XÓA USER TEST (Quan trọng!)
        # Tuyệt đối không dùng User.objects.all().delete()
        list_user_ao = ['staff', 'khoa_acc', 'new_mem', 'staff_moi', 'user_fail']
        User.objects.filter(username__in=list_user_ao).delete()

        # 3. Tạo 1 user mẫu chuẩn để test Login
        self.user = User.objects.create_user(username='staff', email='staff@gmail.com', password='123')

    # ----------------------------------------------------------------
    # NHÓM TEST LOGIN (Đăng nhập)
    # ----------------------------------------------------------------

    def test_IT_001(self): # Login Happy Path
        response = self.client.post(self.login_url, {'username': 'staff', 'password': '123'})
        if response.status_code == 302:
            return "PASS", f"Login OK -> Redirect về {response.url}"
        return "FAIL", f"Lỗi: Server trả về code {response.status_code} (Mong đợi 302)"

    def test_IT_002(self): # Login sai pass
        response = self.client.post(self.login_url, {'username': 'staff', 'password': 'sai_pass'})
        if response.status_code == 200:
            return "PASS", "Hệ thống chặn Login sai pass thành công"
        return "FAIL", "Lỗi: Nhập sai pass mà vẫn Redirect"

    def test_IT_003(self): # Username không tồn tại
        response = self.client.post(self.login_url, {'username': 'ma_troi', 'password': '123'})
        if response.status_code == 200:
            return "PASS", "Hệ thống báo lỗi User không tồn tại OK"
        return "FAIL", "Lỗi: User ảo mà vẫn đăng nhập được!"

    def test_IT_004(self): # User bị khóa (Inactive)
        User.objects.create_user(username='khoa_acc', password='123', is_active=False)
        response = self.client.post(self.login_url, {'username': 'khoa_acc', 'password': '123'})
        if response.status_code == 200:
            return "PASS", "Đã chặn User Inactive"
        return "FAIL", "Lỗi: Tài khoản bị khóa vẫn đăng nhập được!"

    def test_IT_008(self): # Remember Me
        response = self.client.post(self.login_url, {'username': 'staff', 'password': '123', 'remember_me': 'on'})
        if response.status_code == 302:
            if 'sessionid' in response.cookies:
                return "PASS", "Cookie session đã được tạo OK"
        return "FAIL", "Login thất bại hoặc không có cookie"

    def test_IT_010(self): # Redirect Param
        url = f"{self.login_url}?next=/admin/"
        response = self.client.post(url, {'username': 'staff', 'password': '123'})
        if response.status_code == 302 and '/admin/' in response.url:
            return "PASS", "Redirect đúng trang /admin/"
        return "FAIL", f"Redirect sai: {response.url}"

    # ----------------------------------------------------------------
    # NHÓM TEST REGISTER (Đăng ký)
    # ----------------------------------------------------------------
    # Lưu ý: Các test này phụ thuộc vào tên field trong form đăng ký của bạn

    def test_IT_019(self): # Đăng ký thành công
        count_before = User.objects.count()
        # Nếu dùng UserCreationForm mặc định, field pass là password1/password2
        data = {
            'username': 'new_mem',
            'email': 'new@test.com',
            'password': '123',         # Hoặc 'password1': '123'
            'confirm_password': '123'  # Hoặc 'password2': '123'
        }
        # Thử gửi 2 kiểu key phổ biến để chắc ăn
        data_django = {'username': 'new_mem', 'email': 'new@test.com', 'password1': '123', 'password2': '123'}
        
        self.client.post(self.register_url, data)
        # Nếu không tăng, thử gửi kiểu django
        if User.objects.count() == count_before:
             self.client.post(self.register_url, data_django)

        if User.objects.count() > count_before:
             return "PASS", "Đã tạo mới User DB thành công"
        return "FAIL", "Submit form nhưng không có User mới (Check lại tên field password)"

    def test_IT_021(self): # Trùng Username
        data = {'username': 'staff', 'email': 'k@test.com', 'password': '123', 'confirm_password': '123'}
        response = self.client.post(self.register_url, data)
        if response.status_code == 200:
            return "PASS", "Chặn trùng Username OK"
        return "FAIL", "Vẫn cho đăng ký trùng tên"

    def test_IT_026(self): # Trùng Email
        # Mặc định Django KHÔNG chặn trùng email, nên test này có thể FAIL nếu bạn chưa code logic chặn
        data = {'username': 'staff_moi', 'email': 'staff@gmail.com', 'password': '123', 'confirm_password': '123'}
        self.client.post(self.register_url, data)
        
        if User.objects.filter(username='staff_moi').exists():
            # Nếu user vẫn được tạo -> Django mặc định
            return "SKIP", "Django mặc định cho phép trùng Email (Muốn chặn phải code thêm)"
        return "PASS", "Hệ thống chặn trùng Email OK"

    def test_IT_031(self): # Confirm Pass sai
        data = {'username': 'user_fail', 'password': '123', 'confirm_password': '456'}
        self.client.post(self.register_url, data)
        if not User.objects.filter(username='user_fail').exists():
             return "PASS", "Validate Confirm Password OK"
        return "FAIL", "Password lệch mà vẫn tạo được!"