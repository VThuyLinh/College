# CollegeApp/admin.py

from django.contrib import admin
from django.utils.html import format_html  # Import format_html
from .models import *
from django import forms
from django.urls import path


class CollegeAdminSite(admin.AdminSite):
    site_header = 'CollegeAdminSite'


admin_site = CollegeAdminSite(name='CollegeAdminSite')


class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'email', 'role',
        'is_active', 'phone', 'gender', 'display_user_photo'  # Thêm phương thức display_user_photo
    ]
    search_fields = ['email', 'first_name', 'last_name', 'national_id_card']  # Thêm national_id_card vào search
    list_filter = ['role', 'is_active', 'date_joined']  # Thêm role và is_active vào filter
    readonly_fields = ['email', 'password', 'date_joined']  # user_photo không nên là readonly nếu bạn muốn upload

    # Phương thức để hiển thị ảnh thumbnail
    def display_user_photo(self, obj):
        if obj.user_photo:
            # Giả sử user_photo lưu URL đầy đủ hoặc đường dẫn tương đối mà STATIC_URL/MEDIA_URL có thể xử lý
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.user_photo)
        return "Không có ảnh"

    # Đặt tên cột hiển thị cho phương thức
    display_user_photo.short_description = 'Ảnh người dùng'

    class Meta:
        model = User
        fields = '__all__'





class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_code', 'first_name', 'last_name', 'major', 'academic_year',
                    'student_status']
    search_fields = ['student_code', 'first_name', 'last_name', 'national_id_card']
    list_filter = ['student_status', 'major', 'academic_year', 'department']

    class Meta:
        model = Student
        fields = '__all__'


class FacultyAdmin(admin.ModelAdmin):  # Thêm FacultyAdmin
    list_display = ['faculty_code', 'first_name', 'last_name', 'type', 'department', 'position']
    search_fields = ['faculty_code', 'first_name', 'last_name', 'national_id_card']
    list_filter = ['type', 'department', 'is_department_head']

    class Meta:
        model = Faculty
        fields = '__all__'


class AdminModelAdmin(admin.ModelAdmin):  # Đổi tên để tránh trùng với model Admin
    list_display = ['admin_code', 'first_name', 'last_name', 'email']
    search_fields = ['admin_code', 'first_name', 'last_name', 'email']
    readonly_fields = ['date_joined']  # Admin có thể tự chỉnh sửa các thông tin khác

    class Meta:
        model = Admin
        fields = '__all__'


class MajorAdmin(admin.ModelAdmin):  # Đổi tên để tránh trùng với model Admin
    list_display = ['name', 'code', 'department']

    class Meta:
        model = Major
        fields = '__all__'


# Đăng ký các model với admin_site của bạn
admin_site.register(User, UserAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Faculty, FacultyAdmin)  # Đăng ký FacultyAdmin
admin_site.register(Admin, AdminModelAdmin)  # Đăng ký AdminModelAdmin

# Đăng ký các model khác (nếu cần)
admin_site.register(Album)
admin_site.register(Image)
admin_site.register(Department)
admin_site.register(Program)
admin_site.register(AdmissionRequirement)
admin_site.register(AdmissionMethod)
admin_site.register(Major, MajorAdmin)
admin_site.register(Course)
admin_site.register(AcademicYear)
admin_site.register(Class)
admin_site.register(Semester)
admin_site.register(CourseOffering)