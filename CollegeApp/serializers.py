# your_app_name/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import *


class StudentCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    national_id_card = serializers.CharField(max_length=12, required=True)

    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'nationality', 'national_id_card',
            'date_of_birth', 'place_of_birth', 'user_photo', 'email', 'phone',
            'gender', 'address', 'district', 'city', 'student_code',
            'parent_name', 'parent_phone', 'program', 'major', 'academic_year',
            'department', 'student_status', 'GPA'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}  # Mật khẩu sẽ được xử lý riêng
        }

    def create(self, validated_data):

        validated_data['role'] = 'SINH_VIEN'

        password = validated_data['national_id_card']
        validated_data['password'] = make_password(password)

        validated_data['is_active'] = True

        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):
        # Xử lý cập nhật các trường thông tin
        for attr, value in validated_data.items():
            if attr == 'password':  # Không cho phép cập nhật mật khẩu qua update chung
                continue
            setattr(instance, attr, value)
        instance.save()
        return instance


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}  # Không trả về mật khẩu khi đọc

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        admin_instance = Admin.objects.create(**validated_data)
        if password is not None:
            admin_instance.set_password(password)
        admin_instance.role = 'ADMIN'  # Đảm bảo role là ADMIN
        admin_instance.is_staff = True
        admin_instance.is_superuser = True
        admin_instance.save()
        return admin_instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        # Cập nhật các trường khác
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password is not None:
            instance.set_password(password)  # Cập nhật mật khẩu mới nếu có
        instance.save()
        return instance


class FacultyCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    national_id_card = serializers.CharField(max_length=12, required=True)

    class Meta:
        model = Faculty
        fields = [
            'first_name', 'last_name', 'nationality', 'national_id_card',
            'date_of_birth', 'place_of_birth', 'user_photo', 'email', 'phone',
            'gender', 'address', 'district', 'city', 'faculty_code', 'type',
            'department', 'position', 'degree', 'office_location', 'is_department_head'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def create(self, validated_data):
        # Thiết lập vai trò mặc định là CBCNV
        validated_data['role'] = 'CBCNV'

        # Mật khẩu mặc định là national_id_card và được băm
        password = validated_data['national_id_card']
        validated_data['password'] = make_password(password)

        # Tình trạng tài khoản mặc định là đang hoạt động
        validated_data['is_active'] = True

        faculty = Faculty.objects.create(**validated_data)
        return faculty

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                continue
            setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "Mật khẩu mới và xác nhận mật khẩu mới không khớp."})
        return data

    def validate_old_password(self, value):
        # Kiểm tra mật khẩu cũ dựa vào user trong context
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Mật khẩu cũ không đúng.")
        return value

    # Rất quan trọng: Phương thức save() này sẽ nhận instance user để cập nhật
    def save(self, **kwargs):
        user = self.context['request'].user  # Lấy user từ request
        user.password = make_password(self.validated_data['new_password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)  # Thay đổi từ username_or_email sang email
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=True
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                ('Vui lòng cung cấp email và mật khẩu.'),
                code='authorization'
            )

        # Sử dụng email để authenticate
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError(
                ('Không thể đăng nhập với thông tin đã cung cấp.'),
                code='authorization'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                ('Tài khoản người dùng này đã bị vô hiệu hóa.'),
                code='authorization'
            )

        data['user'] = user
        return data


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = ['id', 'name', 'code']  # Các trường bạn muốn hiển thị cho Major


class AdvisoryRegistrationSerializer(serializers.ModelSerializer):
    major_of_interest = MajorSerializer(read_only=True)
    major_of_interest_id = serializers.PrimaryKeyRelatedField(
        queryset=Major.objects.all(),
        source='major_of_interest',  # Ánh xạ đến trường major_of_interest trong model
        allow_null=False,
        required=True
    )

    has_graduated_display = serializers.CharField(source='get_has_graduated_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AdvisoryRegistration
        fields = [
            'id', 'full_name', 'phone_number', 'email', 'address',
            'major_of_interest', 'major_of_interest_id',
            'has_graduated', 'has_graduated_display',
            'registration_date', 'status', 'status_display', 'notes'
        ]
        read_only_fields = ['registration_date', 'status', 'notes', 'has_graduated_display', 'status_display']


    def create(self, validated_data):

        validated_data['status'] = 'NEW'
        # Nếu major_of_interest_id không được cung cấp nhưng major_of_interest_id là null trong model
        if 'major_of_interest_id' in validated_data and validated_data['major_of_interest_id'] is None:
            validated_data['major_of_interest'] = None
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('registration_date', None)
        return super().update(instance, validated_data)
