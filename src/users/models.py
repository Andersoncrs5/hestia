import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from src.permissions.models import Permission
from src.shared.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(
        self,
        email: str,
        password: str | None = None,
        **extra_fields,
    ):
        if not email:
            raise ValueError("Email is required.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, BaseModel):
    name = models.CharField(
        max_length=150,
    )

    email = models.EmailField(
        max_length=254,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_superuser = models.BooleanField(
        default=False,
    )

    permissions = models.ManyToManyField(
        Permission,
        through="permissionsUser.PermissionUser",
        related_name="users",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    def has_perm(
        self,
        perm: str,
        obj=None,
    ) -> bool:
        if self.is_superuser:
            return True

        return self.permissions.filter(
            slug=perm,
            is_active=True,
        ).exists()

    def has_module_perms(
        self,
        app_label: str,
    ) -> bool:
        if self.is_superuser:
            return True

        return self.permissions.filter(
            slug__startswith=f"{app_label}.",
            is_active=True,
        ).exists()