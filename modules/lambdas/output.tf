## Secutiry Group Outputs
## =============================================================================
output "vpc_postgres_ingress_all_egress_id" {
  description = "PostgreSQL security group id"
  value       = module.lambda_security_group.vpc_postgres_ingress_all_egress_id
}

## Lambda Outputs
## =============================================================================
# Ingest Lambdas
# ------------------------------------------------------------------------------
output "copy_to_glacier_arn" {
  description = "AWS ARN for the copy_to_glacier lambda."
  value       = aws_lambda_function.copy_to_glacier.arn
}

output "orca_catalog_reporting_arn" {
  description = "AWS ARN for the orca_catalog_reporting lambda."
  value       = aws_lambda_function.orca_catalog_reporting.arn
}

# Reconciliation Lambdas
# ------------------------------------------------------------------------------
output "get_current_archive_list_arn" {
  description = "AWS ARN for the get_current_archive_list lambda."
  value       = aws_lambda_function.get_current_archive_list.arn
}

output "internal_reconcile_report_job_arn" {
  description = "AWS ARN for the internal_reconcile_report_job lambda."
  value       = aws_lambda_function.internal_reconcile_report_job.arn
}

output "internal_reconcile_report_mismatch_arn" {
  description = "AWS ARN for the internal_reconcile_report_mismatch lambda."
  value       = aws_lambda_function.internal_reconcile_report_mismatch.arn
}

output "internal_reconcile_report_orphan_arn" {
  description = "AWS ARN for the internal_reconcile_report_orphan lambda."
  value       = aws_lambda_function.internal_reconcile_report_orphan.arn
}

output "internal_reconcile_report_phantom_arn" {
  description = "AWS ARN for the internal_reconcile_report_phantom lambda."
  value       = aws_lambda_function.internal_reconcile_report_phantom.arn
}

output "perform_orca_reconcile_arn" {
  description = "AWS ARN for the perform_orca_reconcile lambda."
  value       = aws_lambda_function.perform_orca_reconcile.arn
}

# Recovery Lambdas
# ------------------------------------------------------------------------------
output "extract_filepaths_for_granule_arn" {
  description = "AWS ARN for the extract_filepaths_for_granule lambda."
  value       = aws_lambda_function.extract_filepaths_for_granule.arn
}


output "request_files_arn" {
  description = "AWS ARN for the request_files lambda."
  value       = aws_lambda_function.request_files.arn
}


output "copy_files_to_archive_arn" {
  description = "AWS ARN for the copy_files_to_archive lambda."
  value       = aws_lambda_function.copy_files_to_archive.arn
}

output "request_status_for_granule_arn" {
  description = "AWS ARN for the request_status_for_granule lambda."
  value       = aws_lambda_function.request_status_for_granule.arn
}


output "request_status_for_job_arn" {
  description = "AWS ARN for the request_status_for_job lambda."
  value       = aws_lambda_function.request_status_for_job.arn
}

output "post_copy_request_to_queue_arn" {
  description = "AWS ARN for the post_copy_request_to_queue lambda."
  value       = aws_lambda_function.post_copy_request_to_queue.arn
}

# Reporting Lambdas
# ------------------------------------------------------------------------------
output "orca_catalog_reporting_invoke_arn" {
  description = "AWS invoke ARN for orca_catalog_reporting lambda."
  value       = aws_lambda_function.orca_catalog_reporting.invoke_arn
}

output "request_status_for_granule_invoke_arn" {
  description = "AWS invoke ARN for request_status_for_granule lambda."
  value       = aws_lambda_function.request_status_for_granule.invoke_arn
}

output "request_status_for_job_invoke_arn" {
  description = "AWS invoke ARN for request_status_for_job lambda."
  value       = aws_lambda_function.request_status_for_job.invoke_arn
}

output "internal_reconcile_report_job_invoke_arn" {
  description = "AWS invoke ARN for the internal_reconcile_report_job lambda."
  value       = aws_lambda_function.internal_reconcile_report_job.invoke_arn
}

output "internal_reconcile_report_orphan_invoke_arn" {
  description = "AWS invoke ARN for the internal_reconcile_report_orphan lambda."
  value       = aws_lambda_function.internal_reconcile_report_orphan.invoke_arn
}

output "internal_reconcile_report_phantom_invoke_arn" {
  description = "AWS invoke ARN for the internal_reconcile_report_phantom lambda."
  value       = aws_lambda_function.internal_reconcile_report_phantom.invoke_arn
}

output "internal_reconcile_report_mismatch_invoke_arn" {
  description = "AWS invoke ARN for the internal_reconcile_report_mismatch lambda."
  value       = aws_lambda_function.internal_reconcile_report_mismatch.invoke_arn
}
# Utility Lambdas
# ------------------------------------------------------------------------------
output "db_deploy_function_name" {
  description = "AWS Function Name for the db_deploy lambda."
  value       = aws_lambda_function.db_deploy.function_name
}