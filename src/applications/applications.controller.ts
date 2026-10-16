import { Body, Controller, Get, Param, ParseIntPipe, Patch, Post, Query, UseGuards } from '@nestjs/common';
import { ApplicationsService } from './applications.service';
import { CreateApplicationDto } from './dto/create-application.dto';
import { UpdateApplicationStatusDto } from './dto/update-status.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';
import { CurrentUser } from '../auth/decorators/current-user.decorator';

@UseGuards(JwtAuthGuard)
@Controller('applications')
export class ApplicationsController {
  constructor(private apps: ApplicationsService) {}

  @Post()
  create(@CurrentUser('id') id: number, @Body() dto: CreateApplicationDto) {
    return this.apps.create(id, dto);
  }

  @Get('mine')
  mine(@CurrentUser('id') id: number) {
    return this.apps.mine(id);
  }

  @UseGuards(RolesGuard)
  @Roles('ADMIN')
  @Get()
  findAll(@Query('status') status?: string) {
    return this.apps.findAll(status);
  }

  @Get(':id')
  findOne(
    @Param('id', ParseIntPipe) id: number,
    @CurrentUser() user: { id: number; role: string },
  ) {
    return this.apps.findOneForStudent(id, user.id, user.role);
  }

  @UseGuards(RolesGuard)
  @Roles('ADMIN')
  @Patch(':id/status')
  updateStatus(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateApplicationStatusDto,
  ) {
    return this.apps.updateStatus(id, dto);
  }
}
