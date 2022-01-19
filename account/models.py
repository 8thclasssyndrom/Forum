from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models


class UserManager(BaseUserManager):
    def _create(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self,  email, password, **extra_fields):
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(email, password, **extra_fields)


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(primary_key=True)

    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='profile_photo', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    # создание активационного кода, с помощью get_random_string создаем строки из 6 символов
    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(6, '0123456789')
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    # отправка подтверждение о регистрации на почты
    def send_activation_mail(self):
        message = f'Ваш код подтверждения: {self.activation_code}'
        send_mail(
            'Активация аккаунта',
            message,
            'test@gmail.com',
            [self.email]
        )


