# map/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Bank, Branch, ATM, ATMStatus


class TimestampedReadOnlyMixin:
    readonly_fields = ("created_at", "updated_at")


# ------- Inlines -------
class BranchInline(admin.TabularInline):
    model = Branch
    extra = 0
    fields = ("code", "name", "address", "phone", "latitude", "longitude")
    show_change_link = True


class ATMInline(admin.TabularInline):
    model = ATM
    extra = 0
    fields = ("code", "status", "address", "latitude", "longitude")
    show_change_link = True


# ------- Bank -------
@admin.register(Bank)
class BankAdmin(TimestampedReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "phone",
        "address_short",
        "coords",
        "branches_count",
        "created_at",
        "updated_at",
    )
    search_fields = ("code", "name", "address", "phone")
    ordering = ("name",)
    list_per_page = 25
    inlines = [BranchInline]

    def address_short(self, obj):
        if not obj.address:
            return ""
        return obj.address if len(obj.address) <= 60 else obj.address[:60] + "…"
    address_short.short_description = "Địa chỉ"

    def coords(self, obj):
        if obj.latitude is None or obj.longitude is None:
            return ""
        return f"{obj.latitude}, {obj.longitude}"
    coords.short_description = "Lat, Lng"

    def branches_count(self, obj):
        return obj.branches.count()
    branches_count.short_description = "Số CN"


# ------- Branch -------
@admin.register(Branch)
class BranchAdmin(TimestampedReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "bank",
        "phone",
        "coords",
        "atms_count",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "code",
        "name",
        "address",
        "phone",
        "bank__name",
        "bank__code",
    )
    list_filter = ("bank",)
    ordering = ("bank__name", "name")
    list_per_page = 25
    autocomplete_fields = ("bank",)
    list_select_related = ("bank",)
    inlines = [ATMInline]

    def coords(self, obj):
        if obj.latitude is None or obj.longitude is None:
            return ""
        return f"{obj.latitude}, {obj.longitude}"
    coords.short_description = "Lat, Lng"

    def atms_count(self, obj):
        return obj.atms.count()
    atms_count.short_description = "Số ATM"


# ------- ATM -------
@admin.register(ATM)
class ATMAdmin(TimestampedReadOnlyMixin, admin.ModelAdmin):
    list_display = (
        "code",
        "branch",
        "bank_name",
        "status",
        "address_short",
        "coords",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "code",
        "address",
        "branch__name",
        "branch__code",
        "branch__bank__name",
        "branch__bank__code",
    )
    list_filter = ("status", "branch__bank")
    ordering = ("branch__name", "code")
    list_per_page = 25
    autocomplete_fields = ("branch",)
    list_select_related = ("branch", "branch__bank")

    def bank_name(self, obj):
        return obj.branch.bank.name if obj.branch_id else ""
    bank_name.short_description = "Ngân hàng"

    def address_short(self, obj):
        if not obj.address:
            return ""
        return obj.address if len(obj.address) <= 60 else obj.address[:60] + "…"
    address_short.short_description = "Địa chỉ"

    def coords(self, obj):
        if obj.latitude is None or obj.longitude is None:
            return ""
        return f"{obj.latitude}, {obj.longitude}"
    coords.short_description = "Lat, Lng"

    # (Tuỳ chọn) các action nhanh đổi trạng thái
    actions = ["mark_active", "mark_maintenance", "mark_offline"]

    @admin.action(description="Đặt trạng thái: Hoạt động")
    def mark_active(self, request, queryset):
        queryset.update(status=ATMStatus.ACTIVE)

    @admin.action(description="Đặt trạng thái: Bảo trì")
    def mark_maintenance(self, request, queryset):
        queryset.update(status=ATMStatus.MAINTENANCE)

    @admin.action(description="Đặt trạng thái: Offline")
    def mark_offline(self, request, queryset):
        queryset.update(status=ATMStatus.OFFLINE)


# Tuỳ chọn: trang admin header
admin.site.site_header = "Quản trị MapBank"
admin.site.site_title = "MapBank Admin"
admin.site.index_title = "Bảng điều khiển"
