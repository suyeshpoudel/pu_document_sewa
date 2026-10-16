from django.db import models


class DocumentType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    fee_rs = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    required_docs = models.JSONField(default=list)
    processing_days = models.PositiveIntegerField(default=7)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "document types"
        ordering = ["name"]

    def __str__(self):
        return self.name
