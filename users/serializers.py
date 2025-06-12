from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'password': {'write_only': True},
            'email': {'required': True,
                      'allow_blank': False,
                      'validators':
                          [validators.UniqueValidator(
                              User.objects.all(),
                              "A user with that email already exists."
                          )]
                      },
        }

    def create(self, validated_data):
        """
        Create and return a new user instance using Django's create_user.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailing and updating logged in user details.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        read_only_fields = ['username']


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password when logged in.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        # Verify if user sent correct old password
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, data):
        """
        Validate that the new password is different from the old password.
        """
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError(
                "New password must be different from old password."
            )
        return data

    def save(self, **kwargs):
        """
        Save the user's new password.
        """
        password = self.validated_data['new_password']  # type:ignore
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset when logged off.
    """
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        # Validate if there is a user with that email
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "There is no user with that email."
            )
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset when logged off.
    """
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        # Decode uid and validate token sent on request
        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = User.objects.get(pk=uid)
        except (ValueError, TypeError, OverflowError, User.DoesNotExist):
            user = None

        if user is None or not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError(
                "Invalid/Expired password request"
            )

        data['user'] = user
        return data

    def save(self):
        # Retrieve validated data and define new password
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user
