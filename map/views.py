# map/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db.models import Q

from .models import ATM, Bank, Branch
import json


def _fmt(dt):
    """Đưa datetime về chuỗi theo múi giờ local (VD: Asia/Ho_Chi_Minh)."""
    if not dt:
        return ""
    try:
        return timezone.localtime(dt).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        # Phòng khi USE_TZ=False hoặc dt là naive
        return dt.strftime("%Y-%m-%d %H:%M:%S")


@login_required
def map_view(request):
    """Trang chính: render dữ liệu ban đầu để vẽ marker & đổ dropdown."""
    # BANKS: đầy đủ trường trong model + ngày tạo/cập nhật
    banks = []
    for b in Bank.objects.all().order_by("name"):
        banks.append({
            "id": b.id,
            "code": b.code,
            "name": b.name,
            "address": b.address,
            "phone": b.phone,
            "image": b.image,
            "latitude": b.latitude,
            "longitude": b.longitude,
            "created_at": _fmt(b.created_at),
            "updated_at": _fmt(b.updated_at),
        })

    # BRANCHES: đầy đủ + thông tin ngân hàng (name/code/id)
    branches = []
    for br in Branch.objects.select_related("bank").order_by("bank__name", "name"):
        branches.append({
            "id": br.id,
            "code": br.code,
            "name": br.name,
            "address": br.address,
            "phone": br.phone,
            "image": br.image,
            "latitude": br.latitude,
            "longitude": br.longitude,
            "created_at": _fmt(br.created_at),
            "updated_at": _fmt(br.updated_at),
            "bank_id": br.bank_id,
            "bank__name": br.bank.name if br.bank_id else "",
            "bank__code": br.bank.code if br.bank_id else "",
        })

    # ATMS: đầy đủ + thông tin chi nhánh/ngân hàng liên quan + nhãn trạng thái
    atms = []
    for a in ATM.objects.select_related("branch", "branch__bank"):
        atms.append({
            "id": a.id,
            "code": a.code,
            "status": a.status,
            "status_label": a.get_status_display(),
            "address": a.address,
            "image": a.image,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "created_at": _fmt(a.created_at),
            "updated_at": _fmt(a.updated_at),
            "branch_id": a.branch_id,
            "branch__name": a.branch.name if a.branch_id else "",
            "branch__code": a.branch.code if a.branch_id else "",
            "branch__bank_id": a.branch.bank_id if a.branch_id and a.branch.bank_id else None,
            "branch__bank__name": a.branch.bank.name if a.branch_id and a.branch.bank_id else "",
            "branch__bank__code": a.branch.bank.code if a.branch_id and a.branch.bank_id else "",
        })

    ctx = {
        "banks_json":    mark_safe(json.dumps(banks, ensure_ascii=False)),
        "branches_json": mark_safe(json.dumps(branches, ensure_ascii=False)),
        "atms_json":     mark_safe(json.dumps(atms, ensure_ascii=False)),
    }
    return render(request, "map/map_view.html", ctx)


# -------------------- BANK --------------------
@login_required
@require_http_methods(["POST"])
def bank_save(request):
    """
    Tạo/cập nhật Ngân hàng.
    Body: bank_id (optional), code, name, address, phone, image, latitude, longitude
    """
    data = request.POST
    bank_id = (data.get("bank_id") or "").strip()
    code    = (data.get("code") or "").strip()
    name    = (data.get("name") or "").strip()
    address = (data.get("address") or "").strip()
    phone   = (data.get("phone") or "").strip()
    image   = (data.get("image") or "").strip()

    try:
        lat = float(data.get("latitude"))
        lng = float(data.get("longitude"))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "msg": "latitude/longitude invalid"}, status=400)

    if bank_id:
        try:
            bank = Bank.objects.get(id=bank_id)
        except Bank.DoesNotExist:
            return JsonResponse({"ok": False, "msg": "bank not found"}, status=400)
    else:
        bank = Bank()

    bank.code      = code
    bank.name      = name
    bank.address   = address
    bank.phone     = phone
    bank.image     = image
    bank.latitude  = lat
    bank.longitude = lng
    bank.save()

    return JsonResponse({"ok": True, "id": bank.id, "msg": "updated" if bank_id else "created"})


@login_required
@require_http_methods(["POST"])
def bank_delete(request):
    bank_id = (request.POST.get("bank_id") or "").strip()
    if not bank_id:
        return JsonResponse({"ok": False, "msg": "bank_id required"}, status=400)
    try:
        Bank.objects.get(id=bank_id).delete()
    except Bank.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "bank not found"}, status=400)
    return JsonResponse({"ok": True, "msg": "deleted"})


# -------------------- BRANCH --------------------
@login_required
@require_http_methods(["POST"])
def branch_save(request):
    """
    Tạo/cập nhật Chi nhánh.
    Body: branch_id (optional), bank, code, name, address, phone, image, latitude, longitude
    """
    data = request.POST
    branch_id = (data.get("branch_id") or "").strip()
    bank_id   = data.get("bank")
    code      = (data.get("code") or "").strip()
    name      = (data.get("name") or "").strip()
    address   = (data.get("address") or "").strip()
    phone     = (data.get("phone") or "").strip()
    image     = (data.get("image") or "").strip()

    try:
        lat = float(data.get("latitude"))
        lng = float(data.get("longitude"))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "msg": "latitude/longitude invalid"}, status=400)

    try:
        bank = Bank.objects.get(id=bank_id)
    except Bank.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "bank not found"}, status=400)

    if branch_id:
        try:
            br = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return JsonResponse({"ok": False, "msg": "branch not found"}, status=400)
    else:
        br = Branch()

    br.bank      = bank
    br.code      = code
    br.name      = name
    br.address   = address
    br.phone     = phone
    br.image     = image
    br.latitude  = lat
    br.longitude = lng
    br.save()

    return JsonResponse({"ok": True, "id": br.id, "msg": "updated" if branch_id else "created"})


@login_required
@require_http_methods(["POST"])
def branch_delete(request):
    branch_id = (request.POST.get("branch_id") or "").strip()
    if not branch_id:
        return JsonResponse({"ok": False, "msg": "branch_id required"}, status=400)
    try:
        Branch.objects.get(id=branch_id).delete()
    except Branch.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "branch not found"}, status=400)
    return JsonResponse({"ok": True, "msg": "deleted"})


# -------------------- ATM --------------------
@login_required
@require_http_methods(["POST"])
def atm_save(request):
    """
    Tạo/cập nhật ATM.
    Body: atm_id (optional), branch, code, status, address, image, latitude, longitude
    """
    data = request.POST
    atm_id    = (data.get("atm_id") or "").strip()
    branch_id = data.get("branch")
    code      = (data.get("code") or "").strip()
    status    = (data.get("status") or "active").strip()
    address   = (data.get("address") or "").strip()
    image     = (data.get("image") or "").strip()

    try:
        lat = float(data.get("latitude"))
        lng = float(data.get("longitude"))
    except (TypeError, ValueError):
        return JsonResponse({"ok": False, "msg": "latitude/longitude invalid"}, status=400)

    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "branch not found"}, status=400)

    if atm_id:
        try:
            atm = ATM.objects.get(id=atm_id)
        except ATM.DoesNotExist:
            return JsonResponse({"ok": False, "msg": "atm not found"}, status=400)
    else:
        atm = ATM()

    atm.branch    = branch
    atm.code      = code
    atm.status    = status
    atm.address   = address
    atm.image     = image
    atm.latitude  = lat
    atm.longitude = lng
    atm.save()

    return JsonResponse({"ok": True, "id": atm.id, "msg": "updated" if atm_id else "created"})


@login_required
@require_http_methods(["POST"])
def atm_delete(request):
    atm_id = (request.POST.get("atm_id") or "").strip()
    if not atm_id:
        return JsonResponse({"ok": False, "msg": "atm_id required"}, status=400)
    try:
        ATM.objects.get(id=atm_id).delete()
    except ATM.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "atm not found"}, status=400)
    return JsonResponse({"ok": True, "msg": "deleted"})


@login_required
def atms_of_bank(request):
    """Trả về danh sách các ATM thuộc ngân hàng."""
    bank_id = request.GET.get('bank_id')
    if not bank_id:
        return JsonResponse({"ok": False, "msg": "bank_id required"}, status=400)

    try:
        bank = Bank.objects.get(id=bank_id)
    except Bank.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "Bank not found"}, status=400)

    # Lọc các ATM thuộc ngân hàng
    atms = ATM.objects.filter(branch__bank=bank)
    data = list(atms.values('id', 'code', 'latitude', 'longitude', 'status'))

    return JsonResponse(data, safe=False)


# map/views.py
from django.http import JsonResponse
from .models import ATM, Bank

def get_atms_by_bank(request, bank_id):
    """Trả về danh sách ATM của ngân hàng với bank_id."""
    try:
        bank = Bank.objects.get(id=bank_id)
        atms = ATM.objects.filter(branch__bank=bank)
        
        # Nếu không có ATM nào
        if not atms:
            return JsonResponse({"ok": False, "msg": f"No ATMs found for bank {bank_id}"}, status=404)

        # Chuẩn bị dữ liệu trả về
        atms_data = []
        for atm in atms:
            atms_data.append({
                'id': atm.id,
                'code': atm.code,
                'status': atm.status,
                'address': atm.address,
                'latitude': atm.latitude,
                'longitude': atm.longitude,
                'branch_name': atm.branch.name if atm.branch else "",
                'bank_name': atm.branch.bank.name if atm.branch and atm.branch.bank else "",
                'image': atm.image.url if atm.image else "",
            })

        return JsonResponse(atms_data, safe=False)

    except Bank.DoesNotExist:
        return JsonResponse({"ok": False, "msg": "Bank not found"}, status=400)
    except Exception as e:
        return JsonResponse({"ok": False, "msg": str(e)}, status=400)



from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

@user_passes_test(lambda u: u.is_superuser)
def manage_permissions(request):
    # Nếu gửi POST → cập nhật quyền Superuser
    if request.method == "POST":
        uid = request.POST.get("user_id")
        try:
            user = User.objects.get(id=uid)
            user.is_superuser = not user.is_superuser  # đảo trạng thái
            user.save()
        except User.DoesNotExist:
            pass
        return redirect("manage_permissions")

    # GET → hiển thị danh sách người dùng
    users = User.objects.all().order_by("id")
    return render(request, "map/permissions.html", {"users": users})

