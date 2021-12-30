from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import CIEmailField

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})


class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    SALES = "sa"
    SUPPORT = "su"

    USER_TYPE = (
        (SALES, 'Sales'), (SUPPORT, 'Support')
        )

    email = CIEmailField(
        "email address",
        unique=True,
        max_length=100,
        help_text="Required. 100 characters or fewer.",
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )

    first_name = models.CharField("first name", max_length=25)
    last_name = models.CharField("last name", max_length=25)

    # TODO: func - check entered phone number
    phone_number = models.CharField("phone nomber", max_length=20)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    role = models.CharField(choices=USER_TYPE, max_length=10)

    date_created = models.DateTimeField("date joined", default=timezone.now)
    # TODO: func - update updated
    date_updated = models.DateTimeField("date joined", default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.username = self.__class__.objects.normalize_email(self.username.lower())
