from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,
                                     required=True)
    password_confirm = serializers.CharField(min_length=6,
                                             required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email уже занят')
        return email

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self):
        user = User.objects.create_user(**self.validated_data)
        user.create_activation_code()
        user.send_activation_mail()


class ActivationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6,
                                 min_length=6,
                                 required=True)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def activate(self):
        code = self.validated_data.get('code')
        user = User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if not user.is_active:
            raise serializers.ValidationError('Аккаунт не активен')
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=6)
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField(min_length=6)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Укажите верный текущий пароль')
        return old_password

    def validate(self, validated_data):
        new_password = validated_data.get('new_password')
        new_password_confirm = validated_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Неверный пароль или его подтверждение')
        return validated_data

    def set_new_password(self):
        new_password = self.validated_data.get('new_password')
        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с данным email не зарегистрирован')
        return email

    def send_email(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.send_activation_mail()


class ForgotPasswordCompletelySerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(min_length=6)
    new_password_confirm = serializers.CharField(min_length=6)

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def validate(self, validated_data):
        new_password = validated_data.get('new_password')
        new_password_confirm = validated_data.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError('Неверный пароль или его подтверждение')
        return validated_data

    def set_new_password(self):
        code = self.validated_data.get('code')
        new_password = self.validated_data.get('new_password')
        user = User.objects.get(activation_code=code)
        user.set_password(new_password)
        user.save()


class EditProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'country', 'image', 'bio')

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.country = validated_data['country']
        instance.image = validated_data['image']
        instance.bio = validated_data['bio']
        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
