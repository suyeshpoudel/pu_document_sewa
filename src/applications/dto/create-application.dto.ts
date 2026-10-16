import { IsArray, IsInt, IsOptional, IsString, Min, ValidateNested, ArrayMinSize } from 'class-validator';
import { Type } from 'class-transformer';

export class ApplicationFileInput {
  @IsString()
  fileType: string;

  @IsString()
  fileUrl: string;
}

export class CreateApplicationDto {
  @IsInt()
  documentTypeId: number;

  @IsOptional()
  @IsInt()
  collegeId?: number;

  @IsString()
  fullName: string;

  @IsString()
  symbolNo: string;

  @IsString()
  regNo: string;

  @IsString()
  program: string;

  @IsOptional()
  @IsInt()
  passedYear?: number;

  @IsOptional()
  @IsInt()
  @Min(1)
  copies?: number;

  @IsString()
  phone: string;

  @IsString()
  deliveryProvince: string;

  @IsString()
  deliveryDistrict: string;

  @IsString()
  deliveryMunicipality: string;

  @IsOptional()
  @IsInt()
  deliveryWard?: number;

  @IsOptional()
  @IsString()
  deliveryStreet?: string;

  @IsOptional()
  @IsString()
  deliveryNotes?: string;

  @IsOptional()
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => ApplicationFileInput)
  files?: ApplicationFileInput[];
}
