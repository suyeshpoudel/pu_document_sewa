import { IsEmail, IsInt, IsOptional, IsString, MinLength } from 'class-validator';

export class RegisterDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;

  @IsString()
  name: string;

  @IsOptional()
  @IsString()
  phone?: string;

  @IsOptional()
  @IsInt()
  collegeId?: number;

  @IsOptional()
  @IsString()
  symbolNo?: string;

  @IsOptional()
  @IsString()
  regNo?: string;
}
