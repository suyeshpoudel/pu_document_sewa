from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from config.pricing import MINIMUM_SERVICE_FEE_RS


class DocumentType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    fee_rs = models.PositiveIntegerField(
        verbose_name="Minimum service fee (Rs.)",
        validators=[MinValueValidator(MINIMUM_SERVICE_FEE_RS)],
        help_text=(
            "Starting pickup & delivery fee for this document. Staff confirm the final "
            "fee for each application based on location and urgency."
        ),
    )
    description = models.TextField(blank=True)
    required_docs = models.JSONField(default=list)
    processing_days = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)
    includes = models.ManyToManyField(
        "self",
        symmetrical=False,
        blank=True,
        related_name="bundles",
        help_text="For bundles: the component certificates included (e.g. TMP = Transcript + Migration + Provisional).",
    )

    class Meta:
        verbose_name_plural = "document types"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.pk and self.includes.filter(pk=self.pk).exists():
            raise ValidationError({"includes": "A document cannot include itself."})
