from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email, get_user_model
from allauth.utils import email_address_exists

from django.contrib.auth.forms import PasswordResetForm
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from users.models import USER_TYPE
from users.serializers import UserSerializer

User = get_user_model()

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ('key', 'user', 'created')


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(required=True, choices=USER_TYPE)

    # validate email
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email
    
    # clean password
    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    # get the cleaned data
    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', None),
            'email': self.validated_data.get('email', None),

            'first_name': self.validated_data.get('first_name', None),
            'last_name': self.validated_data.get('last_name', None),

            'type': self.validated_data.get('user_type', None),
        }

    # save the data after validation
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)

        # save the user
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()

        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)

        if not self.reset_form.is_valid():
            raise serializers.ValidationError(
                _('Incorrect information provided'))

        if not User.objects.filter(email=value).exists():

            raise serializers.ValidationError(
                _('This e-mail address does not exists'))
        return value

    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': "host@example.com",

            'email_template_name': 'email_templates/reset_password.html',
            'html_email_template_name': 'email_templates/reset_password.html',
            'request': request,
            'extra_email_context': {'user': User.objects.get(email=self.data.get('email'))}
        }
        self.reset_form.save(**opts)