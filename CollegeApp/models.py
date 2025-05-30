from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'national_id_card','username']
    ROLE_CHOICES = [
        ('SINH_VIEN', 'Sinh viên'),
        ('CBCNV', 'Cán bộ công nhân viên'),
        ('ADMIN', 'Quản trị viên'),
        ('', 'Chưa có'),

    ]

    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
    ]
    first_name = models.CharField(max_length=100, verbose_name="Tên đệm và tên")
    last_name = models.CharField(max_length=100, verbose_name="Họ")
    nationality = models.CharField(max_length=100, verbose_name="Quốc tịch")
    national_id_card = models.CharField(max_length=12, verbose_name="CCCD")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Ngày sinh")
    place_of_birth = models.CharField(max_length=50,null=True, blank=True, verbose_name="Nơi sinh")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="Ngày nhập học/ Ngày vô làm")
    user_photo = models.CharField(max_length=1000,default='',null=True, blank=True,verbose_name="ảnh")
    password = models.CharField(max_length=300, null=True)
    is_active = models.BooleanField(default=1, verbose_name="Tình trạng tài khoản")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=18)
    gender = models.CharField(max_length=50,null=True, blank=True, choices=GENDER_CHOICES, verbose_name="Giới tính")
    address = models.CharField(max_length=200, verbose_name="Địa chỉ (Số nhà,đường, phường)")
    district = models.CharField(max_length=200, verbose_name="Quận/Huyện")
    city = models.CharField(max_length=200, verbose_name="Thành phố/ Tỉnh")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='SINH_VIEN', verbose_name="Loại")
    date_joined = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = "Các Người Dùng"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Album(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tên Album")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả Album")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Các Album"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Image(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tiêu đề ảnh")
    image_file = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả ảnh")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tải lên")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    albums = models.ManyToManyField(Album, related_name='images')

    class Meta:
        verbose_name = "Hình ảnh"
        verbose_name_plural = "Các Hình ảnh"
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"


class Department(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Tên Khoa")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã Khoa")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    established_date = models.DateField(blank=True, null=True, verbose_name="Ngày thành lập")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name="Email")
    website = models.URLField(max_length=200, blank=True, null=True, verbose_name="Website")

    class Meta:
        verbose_name = "Khoa"
        verbose_name_plural = "Các Khoa"
        ordering = ['name']

    def __str__(self):
        return self.name


class Faculty(User):
    FACULTY_TYPE_CHOICES = [
        ('GIANG_VIEN', 'Giảng viên'),
        ('NHAN_VIEN_HANH_CHINH', 'Nhân viên hành chính'),
        ('NGHIEN_CUU_VIEN', 'Nghiên cứu viên'),
        ('THINH_GIANG', 'Thỉnh giảng'),
        ('KHAC', 'Khác'),
    ]

    faculty_code = models.CharField(max_length=50, unique=True, verbose_name="Mã giảng viên/nhân viên")
    type = models.CharField(max_length=50, choices=FACULTY_TYPE_CHOICES, default='GIANG_VIEN', verbose_name="Loại")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='faculty_members', verbose_name="Khoa")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Chức vụ")
    degree = models.CharField(max_length=100, blank=True, null=True, verbose_name="Học vị")
    office_location = models.CharField(max_length=100, blank=True, null=True, verbose_name="Địa điểm văn phòng")
    is_department_head = models.BooleanField(default=False, verbose_name="Là trưởng khoa")

    class Meta:
        verbose_name = "Giảng viên/Nhân viên"
        verbose_name_plural = "Giảng viên và Nhân viên"
        ordering = ['last_name', 'first_name']  # Sắp xếp theo họ, sau đó là tên

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.faculty_code})"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"


class Program(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('CHINH_QUY', 'Chính quy'),
        ('PHO_THONG_CAO_DANG', 'Phổ thông cao đẳng 9+'),
        ('LIEN_THONG_VAN_BANG_2_CAO_DANG', 'Liên thông/Văn bằng 2 cao đẳng'),
        ('LIEN_THONG_VAN_BANG_2_DAI_HOC', 'Liên thông/Văn bằng 2 đại học'),
    ]

    name = models.CharField(max_length=50, choices=PROGRAM_TYPE_CHOICES, default='CAO_DANG_CHINH_QUY',
                            verbose_name="Tên Chương trình")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã Chương trình")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    duration_years = models.IntegerField(blank=True, null=True, verbose_name="Thời lượng (năm)")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")

    class Meta:
        verbose_name = "Chương trình đào tạo"
        verbose_name_plural = "Các Chương trình đào tạo"
        ordering = ['name']

    def __str__(self):
        return self.name


class AdmissionRequirement(models.Model):
    REQUIREMENT_CHOICES = [
        ('THPT', 'Đã tốt nghiệp THPT'),
        ('TCMT', 'Đã tốt nghiệp Trung cấp Y học Cổ truyền'),
        ('TC_CD_DH', 'Đã tốt nghiệp bậc trung cấp, cao đẳng, đại học'),
        ('NNYT', 'Người làm việc trong ngành Y tế: Cán bộ y tế, Điều dưỡng, Dược sĩ, Kỹ thuật viên…'),

    ]

    requirement = models.CharField(
        max_length=50,  # Kích thước max_length nên đủ lớn cho giá trị key (ví dụ: 'TC_CD_DH')
        choices=REQUIREMENT_CHOICES,
        unique=True,  # Đảm bảo mỗi yêu cầu là duy nhất
        verbose_name="Đối tượng tuyển sinh"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mô tả chi tiết"
    )

    class Meta:
        verbose_name = "Đối tượng tuyển sinh"
        verbose_name_plural = "Các đối tượng tuyển sinh"
        ordering = ["requirement"]

    def __str__(self):
        # Khi hiển thị, chúng ta muốn hiển thị giá trị mô tả (ví dụ: "Đã tốt nghiệp THPT")
        # Sử dụng get_requirement_display() để lấy giá trị hiển thị từ choices
        return self.get_requirement_display()


class AdmissionMethod(models.Model):
    METHOD_CHOICES = [
        ('ONLINE', 'Đăng ký trực tuyến'),
        ('HOTLINE_ZALO', 'Đăng ký qua Hotline/Zalo'),
        ('DIRECT', 'Đăng ký trực tiếp tại trường'),
        ('OTHER', 'Khác'),
    ]

    method_type = models.CharField(max_length=50, choices=METHOD_CHOICES, unique=True, verbose_name="Loại hình đăng ký")
    description = models.TextField(verbose_name="Mô tả cách thức")
    url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL đăng ký (nếu có)")
    contact_info = models.CharField(max_length=200, blank=True, null=True,
                                    verbose_name="Thông tin liên hệ (Hotline/Zalo)")
    is_active = models.BooleanField(default=True, verbose_name="Đang áp dụng")

    class Meta:
        verbose_name = "Cách thức đăng ký xét tuyển"
        verbose_name_plural = "Các cách thức đăng ký xét tuyển"
        ordering = ['method_type']

    def __str__(self):
        return self.get_method_type_display()







class Major(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Tên Ngành học")
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã Ngành học")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='majors',
                                   verbose_name="Thuộc khoa")
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='majors',
                                verbose_name="Chương trình đào tạo")
    required_credits = models.IntegerField(blank=True, null=True, verbose_name="Số tín chỉ yêu cầu")
    album= models. ForeignKey( Album,blank=True, null=True, verbose_name="album", on_delete=models.CASCADE )

    class Meta:
        verbose_name = "Ngành học/Chuyên ngành"
        verbose_name_plural = "Các Ngành học/Chuyên ngành"
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('BAT_BUOC', 'Bắt buộc'),
        ('TU_CHON', 'Tự chọn'),
        ('DAI_CUONG', 'Đại cương'),
        ('CHUYEN_NGANH', 'Chuyên ngành'),
        ('KHAC', 'Khác'),
    ]

    course_code = models.CharField(max_length=20, unique=True, verbose_name="Mã môn học")
    title = models.CharField(max_length=255, verbose_name="Tên môn học")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    credits = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Số tín chỉ")
    course_type = models.CharField(max_length=50, choices=COURSE_TYPE_CHOICES, default='CHUYEN_NGANH',
                                   verbose_name="Loại môn học")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses',
                                   verbose_name="Khoa quản lý")
    lecturers = models.ManyToManyField(Faculty, blank=True, related_name='teaching_courses',
                                       verbose_name="Giảng viên phụ trách")
    total_hours = models.IntegerField(blank=True, null=True, verbose_name="Tổng số giờ học")
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='required_for',
                                           verbose_name="Môn học tiên quyết")
    major = models.ManyToManyField(Major, blank=True, related_name='major_courses', verbose_name="Thuộc ngành học")

    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Các Môn học"
        ordering = ['course_code']

    def __str__(self):
        return f"{self.course_code} - {self.title}"


class AcademicYear(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên Niên khóa/Khóa học")
    start_year = models.IntegerField(verbose_name="Năm bắt đầu")
    end_year = models.IntegerField(verbose_name="Năm kết thúc")

    class Meta:
        verbose_name = "Niên khóa"
        verbose_name_plural = "Các Niên khóa"
        ordering = ['-start_year', 'name']
        constraints = [
            models.CheckConstraint(check=models.Q(end_year__gt=models.F('start_year')), name='end_year_gt_start_year')
        ]

    def __str__(self):
        return self.name


class Class(models.Model):
    class_name = models.CharField(
        max_length=100, unique=True, verbose_name="Tên Lớp")
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True, blank=True, related_name='classes',
                              verbose_name="Ngành học")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='classes_by_year', verbose_name="Niên khóa")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='classes_by_department', verbose_name="Khoa quản lý")
    end_date = models.DateField(blank=True, null=True, verbose_name="Ngày dự kiến kết thúc")
    number_of_students = models.IntegerField(default=0, verbose_name="Số lượng sinh viên (dự kiến/hiện tại)"
                                             )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Lớp đang hoạt động"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Mô tả lớp"
    )

    class Meta:
        verbose_name = "Lớp học"
        verbose_name_plural = "Các Lớp học"
        ordering = ['-academic_year__start_year', 'class_name']  # Sắp xếp theo niên khóa và tên lớp

    def __str__(self):
        if self.academic_year:
            return f"{self.class_name} ({self.major.name if self.major else 'N/A'}) - {self.academic_year.name}"
        return f"{self.class_name} ({self.major.name if self.major else 'N/A'})"


class Semester(models.Model):
    SEMESTER_TYPE_CHOICES = [
        ('HK1', 'Học kỳ 1'),
        ('HK2', 'Học kỳ 2'),
        ('HK3', 'Học kỳ 3'),
        ('HK4', 'Học kỳ 4'),
        ('HK5', 'Học kỳ 5'),
        ('HK6', 'Học kỳ 6'),
    ]
    name = models.CharField(max_length=100, verbose_name="Tên học kỳ (ví dụ: Học kỳ 1, 2023-2024)")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='semesters',
                                      verbose_name="Niên khóa")
    semester_type = models.CharField(max_length=30, choices=SEMESTER_TYPE_CHOICES, verbose_name="Học kỳ")
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc")

    class Meta:
        verbose_name = "Học kỳ"
        verbose_name_plural = "Các Học kỳ"
        unique_together = ['academic_year', 'semester_type']
        ordering = ['-academic_year__start_year', 'start_date']

    def __str__(self):
        return f"{self.name} - {self.academic_year.name}"


class CourseOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='offerings', verbose_name="Môn học")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='course_offerings',
                                 verbose_name="Học kỳ")
    lecturer = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='taught_offerings', verbose_name="Giảng viên phụ trách")
    class_code = models.CharField(max_length=50, unique=True, verbose_name="Mã lớp học phần")
    max_students = models.IntegerField(verbose_name="Số lượng sinh viên tối đa")
    current_students = models.IntegerField(default=0, verbose_name="Số lượng sinh viên hiện tại")
    schedule = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lịch học (ví dụ: Thứ 2, Tiết 1-3)")
    room = models.CharField(max_length=50, blank=True, null=True, verbose_name="Phòng học")
    start_date = models.DateField(blank=True, null=True, verbose_name="Ngày bắt đầu lớp học phần")
    end_date = models.DateField(blank=True, null=True, verbose_name="Ngày kết thúc lớp học phần")
    is_active = models.BooleanField(default=True, verbose_name="Đang mở")

    class Meta:
        verbose_name = "Lớp học phần"
        verbose_name_plural = "Các Lớp học phần"
        unique_together = ['course', 'semester', 'class_code']
        ordering = ['semester', 'course__title', 'class_code']

    def __str__(self):
        return f"{self.course.title} - {self.class_code} ({self.semester.name})"


class Student(User):
    STUDENT_STATUS_CHOICES = [
        ('DANG_HOC', 'Đang học'),
        ('DA_TOT_NGHIEP', 'Đã tốt nghiệp'),
        ('SAP_TOT_NGHIEP', 'Sắp tốt nghiệp'),
        ('THOI_HOC', 'Đã thôi học'),
        ('BUOC_THOI_HOC', 'Buộc thôi học'),
        ('BAO_LUU', 'Bảo lưu'),

    ]

    student_code = models.CharField(max_length=20, unique=True, verbose_name="Mã số sinh viên")
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=10)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    student_status = models.CharField(max_length=50, choices=STUDENT_STATUS_CHOICES, default='DANG_HOC',
                                      verbose_name="Tình trạng")
    GPA = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True,
                              verbose_name="Điểm trung bình tích lũy (GPA)")

    class Meta:
        verbose_name = "Sinh viên"
        verbose_name_plural = "Sinh viên"
        ordering = ['student_code']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_code})"

    def save(self, *args, **kwargs):
        self.role = 'SINH_VIEN'
        if self._state.adding and self.pk is None:
            self.is_active = True
        super().save(*args, **kwargs)  # Đây là dòng quan trọng

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def academic_standing(self):
        if self.gpa is None:
            return "Chưa có thông tin GPA"

        if self.gpa >= 3.6:
            return "Xuất sắc"
        elif self.gpa >= 3.2:
            return "Giỏi"
        elif self.gpa >= 2.5:
            return "Khá"
        elif self.gpa >= 2.0:
            return "Trung bình"
        elif self.gpa >= 1.5:
            return "Cảnh báo học vụ"
        else:
            return "Buộc thôi học / Đình chỉ"


class Admin(User):
    admin_code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Mã quản trị viên"
    )
    day_start_job = models.DateTimeField(null=False)

    class Meta:
        verbose_name = "Quản trị viên"
        verbose_name_plural = "Quản trị viên"
        ordering = ['last_name', 'first_name']

    def save(self, *args, **kwargs):
        self.role = 'ADMIN'
        if self._state.adding and self.pk is None:
            self.is_active = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name} {self.first_name} (Admin)"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name}"


class AdvisoryRegistration(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Mới đăng ký'),
        ('CONTACTED', 'Đã liên hệ'),
        ('CONSULTED', 'Đã tư vấn'),
    ]

    GRADUATED_CHOICES = [
        ('THCS', 'Trung học cơ sở'),
        ('THPT', 'Trung học phổ thông '),
        ('TC', 'Trung cấp'),
        ('CD', 'Cao đẳng'),
        ('DH', 'Đại học'),
    ]

    full_name = models.CharField(max_length=200, verbose_name="Họ và tên")
    phone_number = models.CharField(max_length=15, verbose_name="Số điện thoại")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Địa chỉ")
    major_of_interest = models.ForeignKey(Major, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Ngành học quan tâm")
    has_graduated = models.CharField(
        max_length=20,
        choices=GRADUATED_CHOICES,
        default='THCS',
        verbose_name="Bạn đã tốt nghiệp ?"
    )
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đăng ký")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW',
        verbose_name="Trạng thái tư vấn"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi chú của tư vấn viên")


    class Meta:
        verbose_name = "Đăng ký tư vấn"
        verbose_name_plural = "Các Đăng ký tư vấn"
        ordering = ['-registration_date'] # Sắp xếp các đăng ký mới nhất lên đầu

    def __str__(self):
        return f"Đăng ký tư vấn của {self.full_name} - {self.get_status_display()}"

