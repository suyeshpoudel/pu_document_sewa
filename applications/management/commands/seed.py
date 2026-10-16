from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from accounts.models import Role
from catalog.models import DocumentType
from colleges.models import College

User = get_user_model()

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
        "fee_rs": 1500,
        "description": "Official academic transcript",
        "required_docs": ["CITIZENSHIP", "MARKSHEET"],
        "processing_days": 7,
    },
    {
        "name": "Provisional Certificate",
        "slug": "provisional",
        "fee_rs": 1000,
        "description": "Provisional pass certificate",
        "required_docs": ["CITIZENSHIP", "MARKSHEET"],
        "processing_days": 5,
    },
    {
        "name": "Migration Certificate",
        "slug": "migration",
        "fee_rs": 1200,
        "description": "For transfer to other university",
        "required_docs": ["CITIZENSHIP", "REG_CARD"],
        "processing_days": 7,
    },
    {
        "name": "Character Certificate",
        "slug": "character",
        "fee_rs": 800,
        "description": "Character certificate",
        "required_docs": ["CITIZENSHIP"],
        "processing_days": 5,
    },
    {
        "name": "Original Degree Certificate",
        "slug": "degree-original",
        "fee_rs": 3000,
        "description": "Convocation degree",
        "required_docs": ["CITIZENSHIP", "TRANSCRIPT", "PROVISIONAL"],
        "processing_days": 30,
    },
    {
        "name": "Correction / Reprint",
        "slug": "correction-reprint",
        "fee_rs": 2000,
        "description": "Name/DOB correction or reprint",
        "required_docs": ["CITIZENSHIP", "OLD_CERT"],
        "processing_days": 14,
    },
]


class Command(BaseCommand):
    help = "Seed colleges, document types, and an admin user"

    def handle(self, *args, **options):
        for c in COLLEGES:
            College.objects.get_or_create(code=c["code"], defaults=c)
        self.stdout.write(self.style.SUCCESS(f"Colleges: {College.objects.count()}"))

        for d in DOCUMENT_TYPES:
            DocumentType.objects.get_or_create(slug=d["slug"], defaults=d)
        self.stdout.write(self.style.SUCCESS(f"Document types: {DocumentType.objects.count()}"))

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
