import { Body, Controller, Get, Post, Query, UseGuards } from '@nestjs/common';
import { DocumentTypesService } from './document-types.service';
import { CreateDocumentTypeDto } from './dto/create-document-type.dto';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { RolesGuard } from '../auth/guards/roles.guard';
import { Roles } from '../auth/decorators/roles.decorator';

@Controller('document-types')
export class DocumentTypesController {
  constructor(private docs: DocumentTypesService) {}

  @Get()
  findAll(@Query('all') all?: string) {
    return this.docs.findAll(all !== '1');
  }

  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('ADMIN')
  @Post()
  create(@Body() dto: CreateDocumentTypeDto) {
    return this.docs.create(dto);
  }
}
