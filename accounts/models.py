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


    def create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('user must have email address')
        email = self.normalize_email(email)
        user = self.model(
                email=email,
                is_staff=is_staff,
                is_superuser=is_superuser,
                **extra_fields
                   )
        # We check if password has been given
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, is_staff=True,
                        is_superuser=True, **extra_fields):
        user=self.create_user(email, password, is_staff, is_superuser, **extra_fields)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    SALES = "sa"
    SUPPORT = "su"
    STAFF = "st"

    USER_TYPE = (
        (SALES, 'Sales'), (SUPPORT, 'Support'), (STAFF, 'Staff')
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
    phone_number = models.CharField("phone number", max_length=20)

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts.")

    role = models.CharField(choices=USER_TYPE, max_length=10, null=True)

    date_created = models.DateTimeField("date created", default=timezone.now)
    # TODO: func - update updated
    date_updated = models.DateTimeField("date updated", default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email.lower())

    def __str__(self):
        return self.email
