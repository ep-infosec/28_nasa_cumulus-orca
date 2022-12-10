# Variables obtained by Cumulus deployment
# Should exist in https://github.com/nasa/cumulus-template-deploy/blob/master/cumulus-tf/variables.tf
# REQUIRED
variable "prefix" {
  type        = string
  description = "Prefix used to prepend to all object names and tags."
}

variable "tags" {
  type        = map(string)
  description = "Tags to be applied to resources that support tags."
}

## variables related to DB and secretsmanager

variable "db_admin_password" {
  description = "Password for RDS database administrator authentication"
  type        = string
}

variable "db_user_name" {
  description = "Username for RDS database user authentication"
  type        = string
}

variable "db_user_password" {
  description = "Password for RDS database user authentication"
  type        = string
}

variable "db_host_endpoint" {
  type        = string
  description = "Database host endpoint to connect to."
}

variable "db_name" {
  type        = string
  description = "The name of the Orca database within the RDS cluster."
}

## variables related to iam roles
variable "restore_object_role_arn" {
  type        = string
  description = "AWS ARN of the restore_object_role."
}

variable "s3_access_key" {
  type        = string
  description = "Access key for communicating with Orca S3 buckets."
}

variable "s3_secret_key" {
  type        = string
  description = "Secret key for communicating with Orca S3 buckets."
}

## Default variable value is set in ../main.tf to disallow any modification.

variable "db_admin_username" {
  description = "Username for RDS database administrator authentication"
  type        = string
}