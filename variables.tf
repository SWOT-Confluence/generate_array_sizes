variable "app_name" {
  type        = string
  description = "Application name"
  default     = "confluence"
}

variable "app_version" {
  type        = number
  description = "The application version number"
  default     = 0.1
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy to"
  default     = "us-west-2"
}

variable "default_tags" {
  type    = map(string)
  default = {}
}

variable "fsap_id" {
  type        = string
  description = "The ID of the EFS file system access point"
}

variable "prefix" {
  type        = string
  description = "Prefix to add to all AWS resources as a unique identifier"
  default     = "confluence"
}
