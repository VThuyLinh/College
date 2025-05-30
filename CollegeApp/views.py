# your_app_name/views.py

from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password  # Cần cho việc đổi mật khẩu
from rest_framework.authtoken.models import Token  # Import cho Token Authentication

# Import tất cả serializers và models bạn đã có
from .serializers import *
from .models import *  # Đảm bảo import các models cần thiết


class StudentCreateAPIView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentCreateSerializer
    permission_classes = [IsAdminUser]


class FacultyCreateAPIView(viewsets.ViewSet, generics.CreateAPIView):
    """
    API để Admin tạo tài khoản Cán bộ Công nhân viên mới.
    Mật khẩu mặc định sẽ là CCCD và được băm.
    Yêu cầu quyền Admin.
    """
    queryset = Faculty.objects.all()
    serializer_class = FacultyCreateSerializer
    permission_classes = [IsAdminUser]  # Chỉ Admin mới được tạo tài khoản cán bộ


class LoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Tạo hoặc lấy Token cho người dùng
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "message": "Đăng nhập thành công!",
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
                "role": user.role
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## Views cho Đổi mật khẩu (Vẫn dùng APIView)


class ChangePasswordAPIView(viewsets.ViewSet, generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()

    def get_object(self):
        # Phương thức này sẽ trả về đối tượng user cần được cập nhật.
        # Đảm bảo chỉ user đang đăng nhập mới có thể đổi mật khẩu của chính họ.
        return self.request.user

    # Ghi đè phương thức `update` để serializer.save() được gọi
    # và trả về phản hồi tùy chỉnh.
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()  # Lấy user hiện tại
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Gọi phương thức save() trong serializer của bạn để băm và lưu mật khẩu
            serializer.save()
            return Response({"message": "Đổi mật khẩu thành công."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdvisoryRegistrationCreateView(viewsets.ViewSet,generics.CreateAPIView):
    queryset = AdvisoryRegistration.objects.all()
    serializer_class = AdvisoryRegistrationSerializer


class AdvisoryRegistrationListView(viewsets.ViewSet,generics.ListAPIView):
    queryset = AdvisoryRegistration.objects.all()
    serializer_class = AdvisoryRegistrationSerializer


class AdvisoryRegistrationDetailView(viewsets.ViewSet,generics.RetrieveUpdateDestroyAPIView):
    queryset = AdvisoryRegistration.objects.all()
    serializer_class = AdvisoryRegistrationSerializer
