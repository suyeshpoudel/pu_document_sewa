import 'dotenv/config';
import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  const colleges = [
    { name: 'Pokhara University Central Campus', code: 'PU- central', district: 'Kaski', address: 'Pokhara' },
    { name: 'Nepal College of Information Technology', code: 'NCIT', district: 'Kathmandu', address: 'Balkumari, Lalitpur' },
    { name: 'Cosmos College of Management and Technology', code: 'COSMOS', district: 'Kathmandu', address: 'Tutunga, Lalitpur' },
  ];
  for (const c of colleges) {
    await prisma.college.upsert({
      where: { code: c.code },
      update: {},
      create: c,
    });
  }

  const docs = [
    { name: 'Transcript', slug: 'transcript', feeRs: 1500, description: 'Official academic transcript', requiredDocs: ['CITIZENSHIP', 'MARKSHEET'], processingDays: 7 },
    { name: 'Provisional Certificate', slug: 'provisional', feeRs: 1000, description: 'Provisional pass certificate', requiredDocs: ['CITIZENSHIP', 'MARKSHEET'], processingDays: 5 },
    { name: 'Migration Certificate', slug: 'migration', feeRs: 1200, description: 'For transfer to other university', requiredDocs: ['CITIZENSHIP', 'REG_CARD'], processingDays: 7 },
    { name: 'Character Certificate', slug: 'character', feeRs: 800, description: 'Character certificate', requiredDocs: ['CITIZENSHIP'], processingDays: 5 },
    { name: 'Original Degree Certificate', slug: 'degree-original', feeRs: 3000, description: 'Convocation degree', requiredDocs: ['CITIZENSHIP', 'TRANSCRIPT', 'PROVISIONAL'], processingDays: 30 },
    { name: 'Correction / Reprint', slug: 'correction-reprint', feeRs: 2000, description: 'Name/DOB correction or reprint', requiredDocs: ['CITIZENSHIP', 'OLD_CERT'], processingDays: 14 },
  ];
  for (const d of docs) {
    await prisma.documentType.upsert({
      where: { slug: d.slug },
      update: { feeRs: d.feeRs, requiredDocs: d.requiredDocs },
      create: d,
    });
  }

  const adminEmail = 'admin@pu.edu.np';
  const existing = await prisma.user.findUnique({ where: { email: adminEmail } });
  if (!existing) {
    await prisma.user.create({
      data: {
        email: adminEmail,
        password: await bcrypt.hash('Admin123!', 10),
        name: 'PU Admin',
        role: 'ADMIN',
      },
    });
    console.log('Seeded admin: admin@pu.edu.np / Admin123!');
  }

  console.log('Seed done');
}

main().finally(() => prisma.$disconnect());
