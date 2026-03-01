from django.db import models


class TimeStampedModel(models.Model):
    """Base model để tự động có created_at / updated_at."""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")


    class Meta:
        abstract = True


class Bank(TimeStampedModel):
    code = models.CharField(
        max_length=20, unique=True, db_index=True,
        verbose_name="Mã ngân hàng"
    )
    name = models.CharField(max_length=120, verbose_name="Tên ngân hàng")
    address = models.CharField(max_length=255, blank=True, verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, blank=True, verbose_name="SĐT")
    image = models.URLField(blank=True, verbose_name="Ảnh (URL)")  # có thể đổi sang ImageField
    latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")

    class Meta:
        verbose_name = "Ngân hàng"
        verbose_name_plural = "Ngân hàng"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Branch(TimeStampedModel):
    bank = models.ForeignKey(
        Bank, on_delete=models.CASCADE, related_name="branches", verbose_name="Ngân hàng"
    )
    code = models.CharField(max_length=20, verbose_name="Mã chi nhánh")
    name = models.CharField(max_length=120, verbose_name="Tên chi nhánh")
    address = models.CharField(max_length=255, verbose_name="Địa chỉ", blank=True)
    phone = models.CharField(max_length=20, verbose_name="SĐT", blank=True)
    image = models.URLField(blank=True, verbose_name="Ảnh (URL)")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")

    class Meta:
        verbose_name = "Chi nhánh"
        verbose_name_plural = "Chi nhánh"
        ordering = ["bank__name", "name"]
        constraints = [
            # Mỗi ngân hàng không được trùng mã chi nhánh
            models.UniqueConstraint(fields=["bank", "code"], name="uq_branch_bank_code"),
        ]
        indexes = [
            models.Index(fields=["bank", "name"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"{self.bank.code}-{self.code} | {self.name}"


class ATMStatus(models.TextChoices):
    ACTIVE = "active", "Hoạt động"
    MAINTENANCE = "maintenance", "Bảo trì"
    OFFLINE = "offline", "Ngừng/Offline"


class ATM(TimeStampedModel):
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="atms", verbose_name="Chi nhánh"
    )
    code = models.CharField(
        max_length=30, unique=True, db_index=True, verbose_name="Mã ATM"
    )
    address = models.CharField(max_length=255, verbose_name="Địa chỉ", blank=True)
    status = models.CharField(
        max_length=20, choices=ATMStatus.choices, default=ATMStatus.ACTIVE, verbose_name="Tình trạng"
    )
    image = models.URLField(blank=True, verbose_name="Ảnh (URL)")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")

    class Meta:
        verbose_name = "ATM"
        verbose_name_plural = "ATM"
        ordering = ["branch__name", "code"]
        indexes = [
            models.Index(fields=["branch", "status"]),
            models.Index(fields=["latitude", "longitude"]),
        ]

    def __str__(self):
        return f"{self.code} @ {self.branch.name}"
