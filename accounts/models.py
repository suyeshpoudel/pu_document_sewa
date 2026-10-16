from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    ADMIN = "ADMIN", "Admin"


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)
    phone = models.CharField(max_length=20, blank=True)
    college = models.ForeignKey(
        "colleges.College", null=True, blank=True, on_delete=models.SET_NULL, related_name="users"
    )
    symbol_no = models.CharField(max_length=50, blank=True)
    reg_no = models.CharField(max_length=50, blank=True)
    citizenship_no = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]

    name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.email

    @property
    def is_staff_role(self):
        return self.role == Role.ADMIN
