import { Body, Controller, Get, Post, UseGuards } from '@nestjs/common';
import { CollegesService } from './colleges.service';
import { CreateCollegeDto } from './dto/create-college.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';

@Controller('colleges')
export class CollegesController {
  constructor(private colleges: CollegesService) {}

  @Get()
  findAll() {
    return this.colleges.findAll();
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('ADMIN')
  @Post()
  create(@Body() dto: CreateCollegeDto) {
    return this.colleges.create(dto);
  }
}
