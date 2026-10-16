from django.conf import settings
from django.db import models


class ApplicationStatus(models.TextChoices):
    SUBMITTED = "SUBMITTED", "Submitted"
    RECEIPT_VERIFIED = "RECEIPT_VERIFIED", "Pickup Receipt Verified"
    COLLECTING = "COLLECTING", "Collecting from PU"
    DISPATCHED = "DISPATCHED", "Dispatched"
    DELIVERED = "DELIVERED", "Delivered"
    REJECTED = "REJECTED", "Rejected"
    CANCELLED = "CANCELLED", "Cancelled"


class Courier(models.TextChoices):
    NEPAL_CAN_MOVE = "NEPAL_CAN_MOVE", "Nepal Can Move"
    FATAK = "FATAK", "Fatak Express"
    OTHER = "OTHER", "Other"


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
    phone = models.CharField(max_length=20)
    pu_reference_no = models.CharField(max_length=100)
    receipt = models.FileField(upload_to="receipts/%Y/%m/")

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

    @property
    def cancelable(self):
        return self.status in (ApplicationStatus.SUBMITTED, ApplicationStatus.RECEIPT_VERIFIED)

    @property
    def timeline(self):
        steps = [
            (ApplicationStatus.SUBMITTED, "Submitted"),
            (ApplicationStatus.RECEIPT_VERIFIED, "Pickup receipt verified"),
            (ApplicationStatus.COLLECTING, "Collecting from PU"),
            (ApplicationStatus.DISPATCHED, "Dispatched"),
            (ApplicationStatus.DELIVERED, "Delivered"),
        ]
        keys = [k for k, _ in steps]
        if self.status in keys:
            current = keys.index(self.status)
        elif self.status in (ApplicationStatus.REJECTED, ApplicationStatus.CANCELLED):
            current = 0
        else:
            current = -1
        return [
            {"key": key, "label": label, "reached": i <= current, "current": i == current}
            for i, (key, label) in enumerate(steps)
        ]


class ApplicationFile(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="files"
    )
    file_type = models.CharField(max_length=50)  # CITIZENSHIP, MARKSHEET, PHOTO, VOUCHER, OTHER
    file = models.FileField(upload_to="applications/%Y/%m/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} for app #{self.application_id}"


class Shipment(models.Model):
    application = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name="shipment"
    )
    courier = models.CharField(
        max_length=30, choices=Courier.choices, default=Courier.NEPAL_CAN_MOVE
    )
    courier_name = models.CharField(max_length=100, blank=True)
    tracking_id = models.CharField(max_length=100, blank=True)
    cod_amount_rs = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, default="PENDING")
    events = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_courier} {self.tracking_id} (app #{self.application_id})"

    @property
    def display_courier(self):
        if self.courier == Courier.OTHER and self.courier_name:
            return self.courier_name
        return self.get_courier_display()

    @property
    def tracking_url(self):
        if self.courier == Courier.NEPAL_CAN_MOVE:
            return "https://portal.nepalcanmove.com/track/"
        return None
