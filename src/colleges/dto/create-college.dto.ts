import { IsOptional, IsString } from 'class-validator';

export class CreateCollegeDto {
  @IsString()
  name: string;

  @IsString()
  code: string;

  @IsString()
  district: string;

  @IsOptional()
  @IsString()
  address?: string;

  @IsOptional()
  @IsString()
  contactEmail?: string;

  @IsOptional()
  @IsString()
  contactPhone?: string;
}
