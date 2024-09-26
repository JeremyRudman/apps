from allauth.account.forms import SignupForm as BaseSignupForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Invisible

from profiles.models import Profile


def validate_is_checked(value):
    if not value:
        raise ValidationError(_("Please read, acknowledge, and confirm by clicking the box"))


class BaseProfileSignupForm(BaseSignupForm):
    first_name = forms.CharField(required=True, label=_("First Name"))
    last_name = forms.CharField(required=True, label=_("Last Name"))
    street_address = forms.CharField(
        max_length=256,
        required=True,
        label=_("Street Address"),
        help_text=Profile._meta.get_field("street_address").help_text,
    )
    zip_code = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r"^(^[0-9]{5}(?:-[0-9]{4})?$|^$)",
                message="Must be a valid zipcode in formats 19107 or 19107-3200",
            )
        ],
        label=_("Zip Code"),
    )
    newsletter_opt_in = forms.BooleanField(
        required=False,
        initial=True,
        help_text=Profile._meta.get_field("newsletter_opt_in").help_text,
    )

    def save(self, request):
        user = super().save(request)
        user.username = user.email
        user.save()
        profile = Profile(
            user=user,
            street_address=self.cleaned_data["street_address"],
            zip_code=self.cleaned_data["zip_code"],
            newsletter_opt_in=self.cleaned_data["newsletter_opt_in"],
        )
        profile.save()
        return user


class ProfileSignupForm(BaseProfileSignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    code_of_conduct = forms.BooleanField(
        label="Code of Conduct",
        help_text=(
            'I have read the <a target="_blank" '
            'href="https://apps.bikeaction.org/policies/code-of-conduct/">'
            "Philly Bike Action Code of Conduct</a>."
        ),
        required=True,
        validators=[validate_is_checked],
    )

    privacy_and_data = forms.BooleanField(
        label="Privacy and Data",
        help_text=(
            'I have read the <a target="_blank" '
            'href="https://apps.bikeaction.org/policies/privacy-and-data/">'
            "Privacy and Data Statement</a>."
        ),
        required=True,
        validators=[validate_is_checked],
    )

    field_order = [
        "first_name",
        "last_name",
        "street_address",
        "zip_code",
        "email",
        "newsletter_opt_in",
        "password1",
        "password2",
        "captcha",
    ]

    class Meta:
        help_texts = {}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "first_name",
            "last_name",
            "email",
            "street_address",
            "zip_code",
            "newsletter_opt_in",
        ]
        help_texts = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["first_name"].initial = kwargs["instance"].user.first_name
        self.fields["last_name"].initial = kwargs["instance"].user.last_name
        self.fields["email"].initial = kwargs["instance"].user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.first_name = self.cleaned_data["first_name"]
        profile.user.last_name = self.cleaned_data["last_name"]
        if commit:
            profile.save()
            profile.user.save()
        return profile

    first_name = forms.CharField(required=True, label=_("First Name"))
    last_name = forms.CharField(required=True, label=_("Last Name"))
    email = forms.EmailField(
        disabled=True,
        required=True,
        help_text=mark_safe('Update your email address <a href="/accounts/email/">here</a>'),
        label=_("Email"),
    )
