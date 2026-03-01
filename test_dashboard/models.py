from django.db import models

class TestCaseDefinition(models.Model):
    TEST_TYPES = [
        ('Unit', 'Unit Test'),
        ('Integration', 'Integration Test'),
        ('System', 'System Test'),
    ]
    
    test_id = models.CharField(max_length=50, unique=True) # Ví dụ: UT_001
    test_type = models.CharField(max_length=20, choices=TEST_TYPES, default='Unit')
    description = models.CharField(max_length=255) # Ví dụ: Nhập tên đăng nhập hợp lệ
    input_data = models.TextField(blank=True, null=True) # Cột Dữ liệu đầu vào bạn yêu cầu thêm
    expected_result = models.CharField(max_length=255) # Kết quả mong đợi
    
    # Mapping với tên hàm trong code thực tế (để tool biết chạy hàm nào)
    # Ví dụ: users.tests.LoginUnitTests.test_UT_001_valid_login
    mapping_method = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.test_id} - {self.description}"

class TestResult(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Đang chờ'),
        ('PASS', 'Thành công'),
        ('FAIL', 'Thất bại'),
        ('ERROR', 'Lỗi hệ thống'),
    ]
    
    test_case = models.ForeignKey(TestCaseDefinition, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    actual_result = models.TextField(blank=True, null=True) # Kết quả thực tế / Ghi chú lỗi
    executed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test_case.test_id} - {self.status}"