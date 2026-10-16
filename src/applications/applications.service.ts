import {
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateApplicationDto } from './dto/create-application.dto';
import { UpdateApplicationStatusDto } from './dto/update-status.dto';

const include = {
  documentType: true,
  college: true,
  files: true,
  payments: true,
  shipment: true,
};

@Injectable()
export class ApplicationsService {
  constructor(private prisma: PrismaService) {}

  async create(studentId: number, dto: CreateApplicationDto) {
    const { files, ...data } = dto;
    return this.prisma.application.create({
      data: {
        ...data,
        studentId,
        status: 'SUBMITTED',
        files: files?.length
          ? { create: files.map((f) => ({ fileType: f.fileType, fileUrl: f.fileUrl })) }
          : undefined,
      },
      include,
    });
  }

  mine(studentId: number) {
    return this.prisma.application.findMany({
      where: { studentId },
      orderBy: { createdAt: 'desc' },
      include,
    });
  }

  async findOneForStudent(id: number, studentId: number, role: string) {
    const app = await this.prisma.application.findUnique({
      where: { id },
      include,
    });
    if (!app) throw new NotFoundException('Application not found');
    if (role !== 'ADMIN' && app.studentId !== studentId) {
      throw new ForbiddenException('Not your application');
    }
    return app;
  }

  findAll(status?: string) {
    return this.prisma.application.findMany({
      where: status ? { status: status as any } : undefined,
      orderBy: { createdAt: 'desc' },
      include: { ...include, student: { select: { id: true, name: true, email: true } } },
    });
  }

  async updateStatus(id: number, dto: UpdateApplicationStatusDto) {
    const app = await this.prisma.application.findUnique({ where: { id } });
    if (!app) throw new NotFoundException('Application not found');
    return this.prisma.application.update({
      where: { id },
      data: {
        status: dto.status,
        adminRemark: dto.adminRemark,
        trackingNo: dto.trackingNo,
      },
      include,
    });
  }
}
