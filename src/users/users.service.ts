import { Injectable, NotFoundException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { PrismaService } from '../prisma/prisma.service';
import { CreateUserDto, UpdateUserDto } from './dto/user.dto';

const select = {
  id: true,
  email: true,
  name: true,
  phone: true,
  role: true,
  collegeId: true,
  symbolNo: true,
  regNo: true,
  createdAt: true,
};

@Injectable()
export class UsersService {
  constructor(private prisma: PrismaService) {}

  async create(dto: CreateUserDto) {
    const password = await bcrypt.hash(dto.password, 10);
    return this.prisma.user.create({ data: { ...dto, password }, select });
  }

  findAll() {
    return this.prisma.user.findMany({ select, orderBy: { id: 'asc' } });
  }

  async findOne(id: number) {
    const user = await this.prisma.user.findUnique({ where: { id }, select });
    if (!user) throw new NotFoundException('User not found');
    return user;
  }

  update(id: number, dto: UpdateUserDto) {
    return this.prisma.user.update({ where: { id }, data: dto, select });
  }

  remove(id: number) {
    return this.prisma.user.delete({ where: { id }, select: { id: true } });
  }
}
