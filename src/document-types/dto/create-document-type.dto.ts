import { IsArray, IsBoolean, IsInt, IsOptional, IsString, Min } from 'class-validator';

export class CreateDocumentTypeDto {
  @IsString()
  name: string;

  @IsString()
  slug: string;

  @IsInt()
  @Min(0)
  feeRs: number;

  @IsOptional()
  @IsString()
  description?: string;

  @IsOptional()
  @IsArray()
  requiredDocs?: string[];

  @IsOptional()
  @IsInt()
  processingDays?: number;

  @IsOptional()
  @IsBoolean()
  isActive?: boolean;
}
