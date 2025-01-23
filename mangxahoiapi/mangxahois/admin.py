from django import forms
from django.contrib import admin
from django.utils.html import mark_safe
from .models import User, BaiDang, BinhLuan, Reaction

class MyAdminSite(admin.AdminSite):
    site_header = 'Hệ thống mạng xã hội'

admin_site = MyAdminSite(name='myadmin')

class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'password', 'email', 'first_name', 'last_name', 'SDT', 'vaiTro', 'image')
    list_display = ['username', 'email', 'SDT', 'vaiTro']
    search_fields = ['username']
    readonly_fields = ['avatar_display']

    def avatar_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No avatar"


class BinhLuanForm(forms.ModelForm):
    class Meta:
        model = BinhLuan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lọc danh sách bài đăng không bị khóa bình luận
        self.fields['baiDang'].queryset = BaiDang.objects.filter(khoa_binh_luan=False)

class BinhLuanAdmin(admin.ModelAdmin):
    form = BinhLuanForm
    list_display = ['baiDang', 'nguoiBinhLuan', 'noiDung', 'created_date']
    search_fields = ['noiDung', 'nguoiBinhLuan__username', 'baiDang__tieuDe']
    list_filter = ['created_date', 'baiDang']

    def has_delete_permission(self, request, obj=None):
        if obj and obj.nguoiBinhLuan == request.user:
            return True  # Người dùng có thể xoá comment của họ
        if obj and obj.baiDang.nguoiDangBai == request.user:
            return True  # Chủ bài viết có thể xoá comment
        return False  # Không cho phép xoá

class BinhLuanInline(admin.TabularInline):
    model = BinhLuan
    extra = 1  # Số lượng trường bình luận mặc định hiển thị
    readonly_fields = ['nguoiBinhLuan', 'noiDung', 'created_date']

class BaiDangAdmin(admin.ModelAdmin):
    list_display = ['tieuDe', 'nguoiDangBai', 'created_date', 'khoa_binh_luan_status']
    search_fields = ['tieuDe']
    list_filter = ['created_date', 'nguoiDangBai']
    actions = ['khoa_binh_luan']
    inlines = [BinhLuanInline]

    def khoa_binh_luan_status(self, obj):
        return obj.khoa_binh_luan
    khoa_binh_luan_status.boolean = True
    khoa_binh_luan_status.short_description = "Bình luận bị khóa?"

    def khoa_binh_luan(self, request, queryset):
        queryset.update(khoa_binh_luan=True)
        self.message_user(request, "Bình luận đã được khóa.")

    khoa_binh_luan.short_description = "Khóa bình luận của bài đăng"

class ReactionAdmin(admin.ModelAdmin):
    list_display = ['baiDang', 'nguoiThucHien', 'loai']
    search_fields = ['baiDang__tieuDe', 'nguoiThucHien__username']
    list_filter = ['loai']

# Đăng ký các models vào trang admin
admin_site.register(User, UserAdmin)
admin_site.register(BaiDang, BaiDangAdmin)
admin_site.register(BinhLuan, BinhLuanAdmin)  # Đăng ký mục Bình luận để quản trị riêng
admin_site.register(Reaction, ReactionAdmin)
