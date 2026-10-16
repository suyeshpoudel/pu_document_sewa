import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateDocumentTypeDto } from './dto/create-document-type.dto';

@Injectable()
export class DocumentTypesService {
  constructor(private prisma: PrismaService) {}

  create(dto: CreateDocumentTypeDto) {
    return this.prisma.documentType.create({ data: dto });
  }

  findAll(activeOnly = true) {
    return this.prisma.documentType.findMany({
      where: activeOnly ? { isActive: true } : undefined,
      orderBy: { feeRs: 'asc' },
    });
  }
}
