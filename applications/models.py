from django.conf import settings
from django.db import models


class ApplicationStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    PAID = "PAID", "Paid"
    PRINTING = "PRINTING", "Printing"
    DISPATCHED = "DISPATCHED", "Dispatched"
    DELIVERED = "DELIVERED", "Delivered"
    CANCELLED = "CANCELLED", "Cancelled"


class PaymentProvider(models.TextChoices):
    ESEWA = "ESEWA", "eSewa"
    KHALTI = "KHALTI", "Khalti"
    BANK_VOUCHER = "BANK_VOUCHER", "Bank Voucher"


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    VERIFIED = "VERIFIED", "Verified"
    FAILED = "FAILED", "Failed"


class Application(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    college = models.ForeignKey(
        "colleges.College", null=True, blank=True, on_delete=models.SET_NULL, related_name="applications"
    )
    document_type = models.ForeignKey(
        "catalog.DocumentType", on_delete=models.PROTECT, related_name="applications"
    )

    full_name = models.CharField(max_length=200)
    symbol_no = models.CharField(max_length=50)
    reg_no = models.CharField(max_length=50)
    program = models.CharField(max_length=200)
    passed_year = models.PositiveIntegerField(null=True, blank=True)
    copies = models.PositiveIntegerField(default=1)

    phone = models.CharField(max_length=20)
    delivery_province = models.CharField(max_length=100)
    delivery_district = models.CharField(max_length=100)
    delivery_municipality = models.CharField(max_length=100)
    delivery_ward = models.PositiveIntegerField(null=True, blank=True)
    delivery_street = models.CharField(max_length=255, blank=True)
    delivery_notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.SUBMITTED
    )
    admin_remark = models.TextField(blank=True)
    tracking_no = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["student", "status"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.full_name} — {self.document_type.name} (#{self.pk})"


class ApplicationFile(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="files"
    )
    file_type = models.CharField(max_length=50)  # CITIZENSHIP, MARKSHEET, PHOTO, VOUCHER, OTHER
    file = models.FileField(upload_to="applications/%Y/%m/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} for app #{self.application_id}"


class Payment(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="payments"
    )
    provider = models.CharField(max_length=20, choices=PaymentProvider.choices)
    amount_rs = models.PositiveIntegerField()
    txn_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    raw_payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} Rs.{self.amount_rs} ({self.status})"


class Shipment(models.Model):
    application = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name="shipment"
    )
    courier = models.CharField(max_length=100, default="MANUAL")
    tracking_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, default="PENDING")
    events = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment #{self.pk} for app #{self.application_id}"
