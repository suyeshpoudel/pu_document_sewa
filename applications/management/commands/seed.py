from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from accounts.models import Role
from catalog.models import DocumentType
from colleges.models import College

User = get_user_model()

SERVICE_FEE_RS = 500

COLLEGES = [
    {
        "name": "Pokhara University Central Campus",
        "code": "PU-CENTRAL",
        "district": "Kaski",
        "address": "Pokhara",
    },
    {
        "name": "Nepal College of Information Technology",
        "code": "NCIT",
        "district": "Kathmandu",
        "address": "Balkumari, Lalitpur",
    },
    {
        "name": "Cosmos College of Management and Technology",
        "code": "COSMOS",
        "district": "Kathmandu",
        "address": "Tutunga, Lalitpur",
    },
]

DOCUMENT_TYPES = [
    {
        "name": "Transcript",
        "slug": "transcript",
        "description": "Official academic transcript, collected from PU and delivered to you.",
        "required_docs": ["CITIZENSHIP", "MARKSHEET"],
        "processing_days": 7,
    },
    {
        "name": "Provisional Certificate",
        "slug": "provisional",
        "description": "Provisional pass certificate.",
        "required_docs": ["CITIZENSHIP", "MARKSHEET"],
        "processing_days": 5,
    },
    {
        "name": "Migration Certificate",
        "slug": "migration",
        "description": "For transfer to other university.",
        "required_docs": ["CITIZENSHIP", "REG_CARD"],
        "processing_days": 7,
    },
    {
        "name": "Character Certificate",
        "slug": "character",
        "description": "Character certificate.",
        "required_docs": ["CITIZENSHIP"],
        "processing_days": 5,
    },
    {
        "name": "Original Degree Certificate",
        "slug": "degree-original",
        "description": "Convocation degree.",
        "required_docs": ["CITIZENSHIP", "TRANSCRIPT", "PROVISIONAL"],
        "processing_days": 30,
    },
    {
        "name": "Correction / Reprint",
        "slug": "correction-reprint",
        "description": "Name/DOB correction or reprint.",
        "required_docs": ["CITIZENSHIP", "OLD_CERT"],
        "processing_days": 14,
    },
]

TMP_BUNDLE = {
    "name": "TMP Bundle (Transcript + Migration + Provisional)",
    "slug": "tmp-bundle",
    "description": (
        "Order Transcript, Migration and Provisional together in a single PU "
        "application (TMP) — one pickup receipt, one delivery."
    ),
    "required_docs": ["CITIZENSHIP", "MARKSHEET", "REG_CARD"],
    "processing_days": 7,
    "includes": ["transcript", "migration", "provisional"],
}


class Command(BaseCommand):
    help = "Seed colleges, document types (minimum service fee), TMP bundle, and an admin user"

    def handle(self, *args, **options):
        for c in COLLEGES:
            College.objects.update_or_create(code=c["code"], defaults=c)
        self.stdout.write(self.style.SUCCESS(f"Colleges: {College.objects.count()}"))

        for d in DOCUMENT_TYPES:
            DocumentType.objects.update_or_create(
                slug=d["slug"],
                defaults={**d, "fee_rs": SERVICE_FEE_RS, "is_active": True},
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Document types: {DocumentType.objects.filter(slug__in=[d['slug'] for d in DOCUMENT_TYPES]).count()} "
                f"(minimum service fee Rs. {SERVICE_FEE_RS})"
            )
        )

        bundle_defaults = {
            k: v for k, v in TMP_BUNDLE.items() if k != "includes"
        }
        bundle_defaults.update({"fee_rs": SERVICE_FEE_RS, "is_active": True})
        bundle, _ = DocumentType.objects.update_or_create(
            slug=TMP_BUNDLE["slug"], defaults=bundle_defaults
        )
        components = DocumentType.objects.filter(
            slug__in=TMP_BUNDLE["includes"]
        ).exclude(pk=bundle.pk)
        bundle.includes.set(components)
        self.stdout.write(
            self.style.SUCCESS(
                f"TMP bundle: {bundle.name} (includes: {', '.join(c.name for c in bundle.includes.all())})"
            )
        )

        if not User.objects.filter(email="admin@pu.edu.np").exists():
            User.objects.create_superuser(
                email="admin@pu.edu.np",
                username="admin@pu.edu.np",
                password="Admin123!",
                name="PU Admin",
                role=Role.ADMIN,
            )
            self.stdout.write(
                self.style.SUCCESS("Seeded admin: admin@pu.edu.np / Admin123!")
            )

        self.stdout.write(self.style.SUCCESS("Seed done"))
