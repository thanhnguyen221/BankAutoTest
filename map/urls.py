from django.urls import path
from . import views

urlpatterns = [
    path("", views.map_view, name="map_view"),

    # BANK
    path("banks/save/", views.bank_save, name="bank_save"),
    path("banks/delete/", views.bank_delete, name="bank_delete"),

    # BRANCH
    path("branches/save/", views.branch_save, name="branch_save"),
    path("branches/delete/", views.branch_delete, name="branch_delete"),

    # ATM
    path("atms/save/", views.atm_save, name="atm_save"),
    path("atms/delete/", views.atm_delete, name="atm_delete"),

    # Lấy ATM theo bank_id
    path('atms/<int:bank_id>/', views.get_atms_by_bank, name='get_atms_by_bank'),

    # Trang phân quyền
    path("permissions/", views.manage_permissions, name="manage_permissions"),
]
