variable "aws_region" {
  description = "AWS region to create the infstructure in"
  default     = "ca-central-1"
}
variable "aws_profile" {
  description = "AWS profile"
}
variable "stack" {
  description = "Name of the stack"
  # default = "fastapi"
}
variable "vpc_cidr" {
  description = "CIDR for VPC"
  default     = "172.17.0.0/16"
}
variable "az_count" {
  description = "# of AZs to cover in a given AWS region"
  default     = "2"
}
variable "aws_ecr" {
  description = "AWS ECR "
}
variable "family" {
  description = "Family of the Task Definition"
  default     = "fastapi"
}
variable "container_port" {
  description = "Port exposed by the docker image to redirect the trrafic to"
  default     = 8000
}
variable "task_count" {
  description = "Number of ECS tasks to run"
  default     = 2
}
variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)"
  default     = "1024"
}
variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)"
  default     = "2048"
}
variable "fargate-task-service-role" {
  description = "Name of the stack."
  // default     = "fastapi"
}
variable "db_instance_type" {
  description = "RDS instance type"
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "RDS DB name"
  default     = "fastapi"
}

variable "db_user" {
  description = "RDS DB username"
  default     = "postgres"
}

# variable "db_password" {
#   description = "RDS DB password"
# }

variable "db_profile" {
  description = "RDS Profile"
  default     = "postgres"
}

variable "db_initialize" {
  description = "RDS initialize"
  default     = "yes"
}

variable "cw_log_group" {
  description = "CloudWatch Log Group"
  default     = "FastApi"
}

variable "cw_log_stream" {
  description = "CloudWatch Log Stream"
  default     = "fargate"
}

variable "source_repo_name" {
  description = "Source repo name"
  type        = string
}

variable "source_repo_branch" {
  description = "Source repo branch"
  type        = string
}

variable "image_repo_name" {
  description = "Image repo name"
  type        = string
}

variable "dockerhub_credentials" {
  type = string
}

variable "codestar_connector_credentials" {
  type = string
}

variable "database_hostname" {
  type = string
}

variable "database_password" {
  type = string
}

variable "database_name" {
  type = string
}

variable "database_port" {
  type = string
}

variable "database_username" {
  type = string
}

variable "secret_key" {
  type = string
}

variable "algorithm" {
  type = string
}

variable "minutes" {
  type = string
}