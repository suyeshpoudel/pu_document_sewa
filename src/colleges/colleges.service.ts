import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';
import { CreateCollegeDto } from './dto/create-college.dto';

@Injectable()
export class CollegesService {
  constructor(private prisma: PrismaService) {}

  create(dto: CreateCollegeDto) {
    return this.prisma.college.create({ data: dto });
  }

  findAll() {
    return this.prisma.college.findMany({ orderBy: { name: 'asc' } });
  }
}
